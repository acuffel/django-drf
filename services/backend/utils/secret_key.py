from random import choice
from string import ascii_letters, digits


def generate_secret_key(lenght: int = 50):
    """Generates a secret key.
    See: https://github.com/django/django/blob/main/django/core/management/utils.py

    Environment variable names used by the utilities in the Shell and Utilities volume
    of IEEE Std 1003.1-2001 consist solely of uppercase letters, digits, and the '_'
    (underscore) from the characters defined in Portable Character Set and do not begin
    with a digit. Other characters may be permitted by an implementation; applications
    shall tolerate the presence of such names.
    """

    secret_key = "".join(
        [choice(ascii_letters)]
        + [choice(ascii_letters + digits + "_") for _ in range(lenght - 1)]
    )

    return secret_key


if __name__ == "__main__":
    secret_key = generate_secret_key()
    print(secret_key)
