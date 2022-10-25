from celery import shared_task

@shared_task(bind=True, queue="computation")
def load_annotations_async(self, annotation_pk: int) -> None:
    from annotations.models import Annotation

    annotation_obj = Annotation.objects.get(pk=annotation_pk)
    annotation_obj.load_annotations_vep()
