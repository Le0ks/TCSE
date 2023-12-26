from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from events.models import Event, EventResults
from homepage.models import New


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "homepage/home.html"

    def get(self, *args, **kwargs):
        context = {}
        context["events"] = Event.objects.filter(author=self.request.user)
        context["event_results"] = EventResults.objects.filter(
            user=self.request.user
        ).only("event")
        return self.render_to_response(context)


class HomepageView(TemplateView):
    template_name = "homepage/homepage.html"

    def get(self, *args, **kwargs):
        context = {}
        context["news"] = New.objects.all()
        return self.render_to_response(context)
