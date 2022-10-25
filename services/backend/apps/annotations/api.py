from rest_framework.routers import APIRootView, DefaultRouter

from annotations.viewsets import AnnotationViewSet, AnnotationVEPViewSet

app_name = "annotations_api"


class AnnotationsAPIRootView(APIRootView):
    pass


class AnnotationsRouter(DefaultRouter):
    APIRootView = AnnotationsAPIRootView


router = AnnotationsRouter()
router.register("annotations", AnnotationViewSet, basename="annotations")
router.register("annotations_vep", AnnotationVEPViewSet, basename="annotations_vep")
urlpatterns = router.urls
