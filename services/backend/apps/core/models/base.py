import uuid

from accounts.models import get_sentinel_user
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # If the related user is deleted, sets the creator to the "deleted" user:
        on_delete=models.SET(get_sentinel_user),
        related_name="%(app_label)s_%(class)ss_as_owner",
        related_query_name="%(app_label)s_%(class)s_as_owner",
        verbose_name=_("owner"),
        help_text=_(
            "The owner of this very object. By default it's the creator of the object."
        ),
        limit_choices_to={"is_active": True},
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("creation date"),
        help_text=_("When was this object created?"),
    )

    changed_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("last modification date"),
        help_text=_("When was this object last modified?"),
    )

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # If the related user is deleted, sets the creator to the "deleted" user:
        on_delete=models.SET(get_sentinel_user),
        related_name="%(app_label)s_%(class)ss_as_changed_by",
        related_query_name="%(app_label)s_%(class)s_as_changed_by",
        verbose_name=_("last editor"),
        help_text=_("Who last modified this object?"),
    )

    class Meta:
        abstract = True
        ordering = ["-changed_at"]
