from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView

from accounts.models import User


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name"]
    template_name = "accounts/profile.html"
    success_message = _("Profile successfully changed.")

    def get_object(self, queryset=None):
        return self.request.user
