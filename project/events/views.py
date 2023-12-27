from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import success, warning
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    View,
)
from events.forms import (
    AnswerForm,
    EventConnectionForm,
    EventForm,
    TaskForm,
    UserAnswerForm,
)
from events.models import (
    Answer,
    Category,
    Event,
    EventResults,
    Tag,
    Task,
    UserAnswer,
)
from events.services import (
    user_can_access_event,
    user_end_event,
    user_is_unregistered_on_event,
)
from slugify import slugify


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "events/list_of_category.html"
    context_object_name = "categories"


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "events/category_detail.html"
    context_object_name = "category"
    slug_url_kwarg = "category_name"


class EventListView(LoginRequiredMixin, ListView):
    queryset = Event.objects.filter(is_private=False)
    template_name = "events/list_of_events.html"
    context_object_name = "events"


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "events/event_detail.html"
    slug_url_kwarg = "event_name"
    context_object_name = "event"

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetailView, self).get_context_data()
        event = context["object"]
        can_access_event = user_can_access_event(event, self.request.user)
        is_register = user_is_unregistered_on_event(event, self.request.user)
        end_event = user_end_event(event, self.request.user)
        context["user_can_access_event"] = can_access_event
        context["user_is_unregistered_on_event"] = is_register
        context["end_event"] = end_event
        return context


class CreateEventListView(LoginRequiredMixin, ListView):
    template_name = "events/create_event.html"
    queryset = Category.objects.filter(is_published=True)
    context_object_name = "categories"


class CreateEventView(LoginRequiredMixin):
    def get(self, *args, **kwargs):
        event = EventForm(prefix="event")
        task_formset = formset_factory(TaskForm, extra=1)(prefix="tasks")
        context = {
            "task_formset": task_formset,
            "event": event,
        }
        answer_formsets = {}
        for index, task in enumerate(task_formset):
            answer_formsets[f"answer-{index + 1}_formset"] = formset_factory(
                AnswerForm, extra=1
            )(prefix=f"answers-{index + 1}")
        context["answer_formsets"] = answer_formsets
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        event = EventForm(self.request.POST or None, prefix="event")
        task_formset = formset_factory(TaskForm)(
            self.request.POST or None, prefix="tasks"
        )
        context = {
            "task_formset": task_formset,
            "event": event,
        }
        answer_formsets = {}
        print(task_formset.errors)
        if event.is_valid() and task_formset.is_valid():
            event_obj = event.save(commit=False)
            event_obj.author = self.request.user
            event_obj.category = Category.objects.get(
                slug=self.get_type_of_task_slug()
            )
            event_obj.slug = slugify(event_obj.name)
            event_obj.is_published = True
            task_objects = []
            answer_objects = []
            tag_objects = []
            formset_valid = True
            for index, task in enumerate(task_formset):
                answer_formset = formset_factory(AnswerForm)(
                    self.request.POST or None, prefix=f"answers-{index + 1}"
                )
                answer_formsets[f"answer-{index + 1}_formset"] = answer_formset
                if task.is_valid() and answer_formset.is_valid():
                    tags = task["tags"].data
                    task_obj = task.save(commit=False)
                    for tag in tags.split():
                        tag_objects.append((tag, task_obj))
                    task_obj.event = event_obj
                    task_obj.task_type = self.get_type_of_task_int()
                    for answer in answer_formset:
                        if answer.is_valid():
                            answer_obj = answer.save(commit=False)
                            answer_obj.task = task_obj
                            answer_objects.append(answer_obj)
                        else:
                            formset_valid = False
                    task_objects.append(task_obj)
                else:
                    formset_valid = False
        else:
            formset_valid = False
        context["answer_formsets"] = answer_formsets
        if formset_valid:
            event_obj.save()
            for task in task_objects:
                task.save()
            for tag in tag_objects:
                Tag.objects.create(name=tag[0], is_published=True, task=tag[1])
            for answer in answer_objects:
                answer.save()
            success(self.request, "Мероприятие успешно создано")
            return redirect(reverse("homepage:home"))
        return self.render_to_response(context)

    def get_type_of_task_slug(self) -> str:
        return

    def get_type_of_task_int(self) -> int:
        return


class CreateTestView(CreateEventView, TemplateView):
    template_name = "events/create_test.html"

    def get_type_of_task_slug(self) -> str:
        return "testwork"

    def get_type_of_task_int(self) -> int:
        return 0


class CreateWrittenWorkView(CreateEventView, TemplateView):
    template_name = "events/create_written_work.html"

    def get_type_of_task_slug(self) -> str:
        return "written_work"

    def get_type_of_task_int(self) -> int:
        return 1


class CreateMixedWorkView(CreateEventView, TemplateView):
    template_name = "events/create_mixed_work.html"

    def get_type_of_task_slug(self) -> str:
        return "mixed_work"

    def get_type_of_task_int(self) -> int:
        return 2


class EventTasksDetailView(LoginRequiredMixin):
    def get(self, *args, **kwargs):
        context = {}
        context["event"] = Event.objects.get(slug=kwargs["event_name"])
        if user_end_event(context["event"], self.request.user):
            return redirect(
                reverse(
                    "events:event_result",
                    kwargs={
                        "category_name": "testwork",
                        "event_name": context["event"].slug,
                    },
                )
            )
        tasks = []
        for task in Task.objects.filter(event=context["event"]):
            if UserAnswer.objects.filter(
                answer__task=task, user=self.request.user
            ).exists():
                tasks.append((task.pk, True))
            else:
                tasks.append((task.pk, False))
        context["tasks"] = tasks
        context["task"] = Task.objects.filter(event=context["event"])[
            kwargs["number_of_task"] - 1
        ]
        context["tags"] = Tag.objects.filter(task=context["task"])
        answers_obj = Answer.objects.filter(task=context["task"])
        answer_formset = self.get_answer_formset(answers_obj, context)
        context["answer_formset"] = answer_formset
        return self.render_to_response(context)

    def post(self, *args, **kwargs):
        context = {}
        context["event"] = Event.objects.get(slug=kwargs["event_name"])
        context["event_result"] = EventResults.objects.get(
            user=self.request.user, event=context["event"]
        )
        context["task"] = Task.objects.filter(event=context["event"])[
            kwargs["number_of_task"] - 1
        ]
        context["tags"] = Tag.objects.filter(task=context["task"])
        answers_obj = Answer.objects.filter(task=context["task"])
        answer_formset = self.post_answer_formset()
        tasks = []
        for task in Task.objects.filter(event=context["event"]):
            if UserAnswer.objects.filter(
                answer__task=task, user=self.request.user
            ).exists():
                tasks.append((task.pk, True))
            else:
                tasks.append((task.pk, False))
        context["tasks"] = tasks
        context["answer_formset"] = answer_formset
        if self.request.POST.get("save_task") is not None:
            for index, answer in enumerate(answers_obj):
                answer_formset[index].fields["is_correct"].label = answer.text
                if answer_formset[index].fields["is_correct"].label == str(
                    UserAnswer.objects.filter(
                        answer=answer, user=self.request.user
                    ).first()
                ):
                    if (
                        UserAnswer.objects.get(
                            answer=answer, user=self.request.user
                        ).is_correct
                        and not answer_formset[index]["is_correct"].data
                    ):
                        context[
                            "event_result"
                        ].number_of_points -= answer.task.number_of_points
                    if (
                        not UserAnswer.objects.get(
                            answer=answer, user=self.request.user
                        ).is_correct
                        and answer_formset[index]["is_correct"].data
                    ):
                        context[
                            "event_result"
                        ].number_of_points += answer.task.number_of_points
                    UserAnswer.objects.filter(
                        answer=answer, user=self.request.user
                    ).update(
                        is_correct=answer_formset[index]["is_correct"].data
                    )
                    context["event_result"].save()
                else:
                    UserAnswer.objects.create(
                        user=self.request.user,
                        answer=answer,
                        is_correct=answer_formset[index]["is_correct"].data,
                    )
                    if UserAnswer.objects.get(
                        answer=answer, user=self.request.user
                    ).is_correct:
                        context[
                            "event_result"
                        ].number_of_points += answer.task.number_of_points
                        context["event_result"].save()
            success(self.request, "Сохранено")
            return self.render_to_response(context)
        if self.request.POST.get("end_event") is not None:
            for task in Task.objects.filter(event=context["event"]):
                if not UserAnswer.objects.filter(
                    answer__task=task, user=self.request.user
                ).exists():
                    warning(self.request, "Выполните все задания")
                    return self.render_to_response(context)
            EventResults.objects.filter(
                user=self.request.user, event=context["event"]
            ).update(is_ended=True)
            return redirect(reverse("homepage:home"))

    def get_answer_formset(self, answerobj, context):
        return

    def post_answer_formset(self):
        return


class TestTasksDetailView(EventTasksDetailView, TemplateView):
    template_name = "events/test_tasks_detail.html"

    def get_answer_formset(self, answers_obj, context):
        answer_formset = formset_factory(
            UserAnswerForm,
            extra=len(answers_obj),
            max_num=len(answers_obj),
            min_num=len(answers_obj),
        )(
            initial=[
                {"text": user_answers.is_correct}
                for user_answers in UserAnswer.objects.filter(
                    answer__task=context["task"],
                    user=self.request.user,
                )
            ]
        )
        for index, answer in enumerate(answers_obj):
            answer_formset[index].fields["is_correct"].label = answer.text
        return answer_formset

    def post_answer_formset(self):
        return formset_factory(UserAnswerForm)(
                self.request.POST or None
            )


class WrittenWorkTasksDetailView(EventTasksDetailView, TemplateView):
    template_name = "events/written_work_tasks_detail.html"

    def get_answer_formset(self, answers_obj, context):
        answer_formset = formset_factory(
            UserAnswerForm,
            extra=len(answers_obj),
            max_num=len(answers_obj),
            min_num=len(answers_obj),
        )(
            initial=[
                {"text": user_answers.is_correct}
                for user_answers in UserAnswer.objects.filter(
                    answer__task=context["task"],
                    user=self.request.user,
                )
            ]
        )
        for index, answer in enumerate(answers_obj):
            answer_formset[index].fields["is_correct"].label = answer.text
        return answer_formset

    def post_answer_formset(self):
        return UserAnswerForm(self.request.POST or None)


class MixedWorkTasksDetailView(EventTasksDetailView, TemplateView):
    template_name = "events/mixed_work_tasks_detail.html"

    def get_answer_formset(self, answers_obj, context):
        answer_formset = UserAnswerForm()
        for index, answer in enumerate(answers_obj):
            answer_formset[index].fields["is_correct"].label = answer.text
        return answer_formset

    def post_answer_formset(self):
        return UserAnswerForm(self.request.POST or None)


class EventRegistrationView(LoginRequiredMixin, View):
    def get(self, request, category_name, event_name):
        event_obj = get_object_or_404(
            Event, slug=event_name, is_published=True
        )
        if user_can_access_event(
            event_obj, request.user
        ) and user_is_unregistered_on_event(event_obj, request.user):
            EventResults.objects.create(
                event=event_obj,
                user=request.user,
            )
            success(
                request,
                f"Регистрация на мероприятие {event_obj.name} прошла успешно!",
            )
            return redirect(
                reverse(
                    "events:event_detail",
                    kwargs={
                        "category_name": event_obj.category.slug,
                        "event_name": event_obj.slug,
                    },
                )
            )
        else:
            raise Http404()


class EventResultView(LoginRequiredMixin, TemplateView):
    template_name = "events/event_result.html"

    def get(self, *args, **kwargs):
        context = {}
        context["event"] = Event.objects.get(slug=kwargs["event_name"])
        event_number_of_points = 0
        tasks = []
        for task in Task.objects.filter(event=context["event"]):
            event_number_of_points += task.number_of_points
            answers_obj = Answer.objects.filter(task=task)
            tags = Tag.objects.filter(task=task)
            answer_formset = formset_factory(
                UserAnswerForm,
                extra=len(answers_obj),
                max_num=len(answers_obj),
                min_num=len(answers_obj),
            )(
                initial=[
                    {"is_correct": user_answers.is_correct}
                    for user_answers in UserAnswer.objects.filter(
                        answer__task=task, user=self.request.user
                    )
                ]
            )
            answers = []
            for index, answer in enumerate(answers_obj):
                answer_formset[index].fields["is_correct"].label = answer.text
                answer_formset[index].fields["is_correct"].widget.attrs[
                    "disabled"
                ] = True
                if (
                    answer.is_correct
                    and UserAnswer.objects.filter(
                        answer=answer, user=self.request.user
                    )
                    .first()
                    .is_correct
                    or (
                        not UserAnswer.objects.filter(
                            answer=answer, user=self.request.user
                        )
                        .first()
                        .is_correct
                        and answer.is_correct
                    )
                ):
                    answers.append((answer_formset[index], 0))
                elif (
                    not answer.is_correct
                    and UserAnswer.objects.filter(
                        answer=answer, user=self.request.user
                    )
                    .first()
                    .is_correct
                ):
                    answers.append((answer_formset[index], 1))
                else:
                    answers.append((answer_formset[index], 2))
            tasks.append((task, tags, answers))
        context["tasks"] = tasks
        context["event_result"] = EventResults.objects.get(
            event=context["event"], user=self.request.user
        )
        context["event_number_of_points"] = event_number_of_points
        context["percent"] = round(
            context["event_result"].number_of_points
            / event_number_of_points
            * 100,
            2,
        )
        return self.render_to_response(context)


class EventRatingView(LoginRequiredMixin, TemplateView):
    template_name = "events/event_rating.html"

    def get(self, *args, **kwargs):
        context = {}
        context["event"] = Event.objects.get(slug=kwargs["event_name"])
        context["event_results"] = EventResults.objects.filter(
            event=context["event"]
        )
        return self.render_to_response(context)


class EventConnectView(LoginRequiredMixin, FormView):
    template_name = "events/event_connect.html"
    form_class = EventConnectionForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            event = get_object_or_404(
                Event, secret_key=form["secret_key"].data
            )
            EventResults.objects.create(
                event=event, user=request.user, is_correct_secret_key=True
            )
            success(request, "Вы зарегестрировались на мероприятие")
            redirect(
                reverse(
                    "events:event_detail",
                    kwargs={
                        "category_name": event.category.slug,
                        "event_name": event.slug,
                    },
                )
            )
        return super().form_valid(form)


class BlankView(LoginRequiredMixin, TemplateView):
    template_name = "events/blank.html"
