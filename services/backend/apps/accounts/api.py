from rest_framework.routers import APIRootView, DefaultRouter

from accounts.viewsets import GroupViewset, PermissionViewset, UserViewset

app_name = "accounts_api"


class AccountsAPIRootView(APIRootView):
    pass


class AccountsRouter(DefaultRouter):
    APIRootView = AccountsAPIRootView


router = AccountsRouter()
router.register("groups", GroupViewset, basename="groups")
router.register("permissions", PermissionViewset, basename="permissions")
router.register("users", UserViewset, basename="users")
urlpatterns = router.urls
