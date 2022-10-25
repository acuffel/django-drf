from rest_framework.routers import APIRootView, DefaultRouter

from assemblies.viewsets import AssemblyViewSet, AssessionViewSet

app_name = "assemblies_api"


class AssembliesAPIRootView(APIRootView):
    pass


class AssembliesRouter(DefaultRouter):
    APIRootView = AssembliesAPIRootView


router = AssembliesRouter()
router.register("assessions", AssessionViewSet, basename="assessions")
router.register("assemblies", AssemblyViewSet, basename="assemblies")
urlpatterns = router.urls

