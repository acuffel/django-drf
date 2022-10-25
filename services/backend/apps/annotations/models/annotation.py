import logging
from itertools import islice
from pathlib import Path

from celery import chain
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from annotations.tasks import load_annotations_async
from assemblies.models import Assembly
from core.models.mixins import VCFMixin, MetadataMixin
from core.tasks import annotation_set_loading_started, annotation_set_loading_success
from vep.utils import get_annotations_vep


logger = logging.getLogger(__name__)

CHARFIELD_MAX_LENGTH = settings.MY_APP_CHAR_MAX_LENGTH


class Annotation(VCFMixin, MetadataMixin):

    assembly = models.ForeignKey(
        Assembly,
        # If Assession is deleted, Annotation will also be deleted:
        on_delete=models.CASCADE,
        related_name="annotations",
        related_query_name="annotation",
        verbose_name=_("assembly"),
    )

    LOADING_FAILURE = 0
    LOADING_PENDING = 1
    LOADING_STARTED = 2
    LOADING_SUCCESS = 3

    LOADING_CHOICES = [
        (LOADING_FAILURE, _("FAILURE")),
        (LOADING_PENDING, _("PENDING")),
        (LOADING_STARTED, _("STARTED")),
        (LOADING_SUCCESS, _("SUCCESS")),
    ]

    loading = models.PositiveSmallIntegerField(
        editable=True,
        choices=LOADING_CHOICES,
        default=LOADING_PENDING,
        verbose_name=_("loading state"),
    )

    class FieldTypeChoices(models.TextChoices):
        BASIC = "basic", _("Basic")
        FULL = "full", _("Full")

    field_type = models.CharField(
        max_length=10,
        choices=FieldTypeChoices.choices,
        default=FieldTypeChoices.BASIC,
        verbose_name=_("field type"),
    )

    class Meta(VCFMixin.Meta, MetadataMixin.Meta):
        verbose_name = _("annotation")
        verbose_name_plural = _("annotations")

    def __str__(self):
        return "Annotation object ({id})".format(id=self.id)

    def get_indexed_vep_cache_path(self):
        return Path(
            f"/code/services/backend/biodb/ftp.ensembl.org/pub/release-106/"
            "variation/indexed_vep_cache"
        )

    def load(self) -> None:
        chain(
            annotation_set_loading_started.si(self.pk),
            load_annotations_async.si(self.pk),
            annotation_set_loading_success.si(self.pk),
        )()

    def load_annotations_vep(self, batch_size: int = 100):
        annotations_vep = get_annotations_vep(self.pk)
        while True:
            batch = list(islice(annotations_vep, batch_size))
            if not batch:
                break
            self.load_annotations_vep_by_batch(annotations_vep=batch)

    def load_annotations_vep_by_batch(self, annotations_vep: list = []):
        from annotations.models import AnnotationVEP

        AnnotationVEP.objects.bulk_create(
            [
                AnnotationVEP(
                    annotation=self,
                    metadata=annotation_vep.dict(),
                )
                for annotation_vep in annotations_vep
            ]
        )

    # loading field methods
    def set_loading_failure(self) -> None:
        self.loading = self.LOADING_FAILURE
        self.save()
        logger.error("Loading failure: %s", self)

    def set_loading_started(self) -> None:
        self.loading = self.LOADING_STARTED
        self.save()
        logger.info("Loading has started: %s", self)

    def set_loading_success(self) -> None:
        self.loading = self.LOADING_SUCCESS
        self.save()
        logger.info("Successfully loaded: %s", self)
