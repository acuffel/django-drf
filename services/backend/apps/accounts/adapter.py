from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site


class CustomUserAccountAdapter(DefaultAccountAdapter):
    """Adapter to enable or disable allauth new signups"""

    def is_open_for_signup(self, request):
        """Checks whether or not the site is open for signups."""

        current_site = get_current_site(request)
        return current_site.sitecustomization.is_open_for_signup
