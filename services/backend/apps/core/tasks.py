import logging

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(ObjectDoesNotExist,),
    retry_kwargs={"max_retries": 10, "countdown": 1},
)
def annotation_set_loading_success(self, annotation_pk: int) -> None:
    from annotations.models import Annotation

    annotations_obj = Annotation.objects.get(pk=annotation_pk)
    annotations_obj.set_loading_success()


@shared_task(
    bind=True,
    autoretry_for=(ObjectDoesNotExist,),
    retry_kwargs={"max_retries": 10, "countdown": 1},
)
def annotation_set_loading_started(self, annotation_pk: int) -> None:
    from annotations.models import Annotation

    annotations_obj = Annotation.objects.get(pk=annotation_pk)
    annotations_obj.set_loading_started()


@shared_task(
    bind=True,
    autoretry_for=(ObjectDoesNotExist,),
    retry_kwargs={"max_retries": 10, "countdown": 1},
)
def load_annotation(self, annotation_pk: int) -> None:
    from annotations.models import Annotation

    annotations_obj = Annotation.objects.get(pk=annotation_pk)

    try:
        annotations_obj.load()
    except NotImplementedError as e:
        logger.warning(e)
        annotations_obj.set_loading_failure()
