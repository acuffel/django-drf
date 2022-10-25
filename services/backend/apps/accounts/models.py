from core.validators import UsernameValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

SENTINEL_USER_USERNAME = "deleted"
BOT_USER_USERNAME = "bot"


def get_sentinel_user():
    user, created = User.objects.get_or_create(
        username=SENTINEL_USER_USERNAME, is_active=False
    )
    return user


def get_bot_user():
    user, created = User.objects.get_or_create(
        username=BOT_USER_USERNAME, is_active=True
    )
    return user


def get_worker_user(hostname):
    username = "worker_{}".format(hostname)
    return User.objects.get_or_create(username=username, is_active=True)[0]


class PublicUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class User(AbstractUser):
    username_validator = UsernameValidator()

    username = models.CharField(
        _("username"),
        primary_key=True,
        max_length=20,
        unique=True,
        help_text=_("Required. 20 characters or fewer. Letters, digits and _ only."),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists.")},
    )

    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
    )

    # MANAGERS
    objects = BaseUserManager()
    public_objects = PublicUserManager()

    class Meta(AbstractUser.Meta):
        ordering = ["-date_joined"]

    def get_absolute_url(self):
        return reverse("accounts:profile")

    def get_avatar_url(self):
        try:
            return self.socialaccount_set.all()[0].get_avatar_url()
        except IndexError:
            return None
