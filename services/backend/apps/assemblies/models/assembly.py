import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.mixins import MetadataMixin

logger = logging.getLogger(__name__)

CHARFIELD_MAX_LENGTH = settings.MY_APP_CHAR_MAX_LENGTH


class Assembly(MetadataMixin):

    # Override the id field to lighten the references to this model:
    id = models.CharField(
        primary_key=True,
        max_length=16,
    )

    class Meta(MetadataMixin.Meta):
        verbose_name = _("assembly")
        verbose_name_plural = _("assemblies")

        ordering = ["id"]


    def __str__(self):
        return str(self.id)
