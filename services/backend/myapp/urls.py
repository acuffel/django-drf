from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

URL_APP_LIST = []

API_PREFIX = "api/v1/vep106/"

API_APP_LIST = [
    "accounts",
]

class DiaghoVepAPIRoot(APIView):
    def get(self, request, format=None):
        return Response(
            {
                app_name: reverse(f"{app_name}_api:api-root", request=request)
                for app_name in API_APP_LIST
            }
        )

# base urls
urlpatterns = [
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

# app urls
urlpatterns += [
    path(f"{API_PREFIX}", DiaghoVepAPIRoot.as_view(), name="api-root"),
    path(
        f"{API_PREFIX}auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
]

# api app urls
urlpatterns += [
    path(f"{API_PREFIX}{app_name}/", include(f"{app_name}.api"))
    for app_name in API_APP_LIST
]

# debug urls
if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
