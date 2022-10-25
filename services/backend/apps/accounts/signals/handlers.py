from accounts.models import User
from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.dispatch import receiver
from django.utils.translation import gettext as _


@receiver(user_signed_up)
def send_mail_to_superusers_when_user_signed_up(request, user, **kwargs):
    superusers = User.objects.filter(is_superuser=True)
    site_name = request.site.name
    site_domain = request.site.domain
    subject = _("[{site_name}] A new user has registered an account").format(
        site_name=site_name
    )
    message = _(
        """Hello from {site_name}!

You're receiving this e-mail because user {username} has registered an
account on {site_domain}, site on which you are referenced as a superuser.

--
{site_name}
"""
    ).format(site_name=site_name, site_domain=site_domain, username=user.username)
    from_email = None
    for superuser in superusers:
        recipient_list = [superuser.email]
        send_mail(subject, message, from_email, recipient_list)
