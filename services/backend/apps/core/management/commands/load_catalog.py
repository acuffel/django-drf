import logging
from typing import Any

from django.core.management import BaseCommand

from assemblies.models import Assession
from core.utils import get_biodb_catalog

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def _load_assessions(self, catalog: dict[str, Any]) -> None:
        Assession.load_catalog(catalog)

    def handle(self, *args, **options) -> None:
        catalog: dict[str, Any] = get_biodb_catalog()
        self._load_assessions(catalog)
