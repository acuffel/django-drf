import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from accounts.models import get_bot_user, get_sentinel_user
from core.models import SiteCustomization


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def _create_site(self):
        example_site = Site.objects.get(pk=1)
        example_site.domain = settings.ALLOWED_HOSTS[0]
        example_site.name = settings.CORE_DEFAULT_SITE_NAME
        SiteCustomization.objects.get_or_create(site=example_site)
        example_site.save()

    def _create_sentinel_user(self):
        get_sentinel_user()

    def _create_bot_user(self):
        get_bot_user()

    def handle(self, *args, **options):
        self._create_site()
        self._create_sentinel_user()
        self._create_bot_user()
