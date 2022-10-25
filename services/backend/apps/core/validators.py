from django.core.validators import RegexValidator
from django.utils.translation import gettext as _


class UsernameValidator(RegexValidator):
    regex = r"^[\w]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, numbers, "
        "and _ character."
    )
    flags = 0


username_validators = [UsernameValidator()]
