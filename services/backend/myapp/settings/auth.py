"""
MyApp authentication settings.
https://docs.djangoproject.com/en/4.0/ref/settings/#auth
"""

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`:
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail:
    "allauth.account.auth_backends.AuthenticationBackend",
)
AUTH_USER_MODEL = "accounts.User"  # Default: "auth.User"
LOGIN_REDIRECT_URL = "core:home"  # Default: "/accounts/profile/"
# LOGIN_URL = "/accounts/login/"
LOGOUT_REDIRECT_URL = (
    "core:home"  # Default: None  # If None, the logout view will be rendered.
)
# PASSWORD_RESET_TIMEOUT = 259200  # 3 days
# PASSWORD_HASHERS = [
#     "django.contrib.auth.hashers.PBKDF2PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
#     "django.contrib.auth.hashers.Argon2PasswordHasher",
#     "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
# ]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
