from django.utils.translation import gettext as _

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = {"title": _("Home")}
        return context
