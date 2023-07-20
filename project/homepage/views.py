from django.views.generic import TemplateView

from .models import New


class HomepageView(TemplateView):
    template_name = "homepage/home.html"

    def get(self, *args, **kwargs):
        context = {}
        context["news"] = New.objects.all()
        return self.render_to_response(context)
