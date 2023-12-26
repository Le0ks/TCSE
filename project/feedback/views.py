from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from feedback.forms import FeedbackForm


class FeedbackView(LoginRequiredMixin, FormView):
    template_name = "feedback/feedback.html"
    form_class = FeedbackForm
    success_url = "/home/"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.send_email(
                user=self.request.user,
                template_name="feedback/email.html",
                subject="Отзыв на сайт tcse.ru",
                message=form["message"].data
            )
        return super().form_valid(form)
