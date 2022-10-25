from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.mixins import MetadataMixin
from annotations.models import Annotation


class AnnotationVEP(MetadataMixin):

    annotation = models.ForeignKey(
        Annotation,
        on_delete=models.CASCADE,
        related_name="annotations_vep",
        related_query_name="annotation_vep",
        verbose_name=_("annotation"),
    )

    class Meta(MetadataMixin.Meta):
        verbose_name = _("annotation_vep")
        verbose_name_plural = _("annotations_vep")

    def __str__(self):
        return _("Annotation object ({id})").format(id=self.id)
