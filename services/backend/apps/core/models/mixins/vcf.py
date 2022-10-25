import logging

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.files.storage import MediaStorage

URLFIELD_MAX_LENGTH = 2048

logger = logging.getLogger(__name__)


def vcf_file_path(instance, filename) -> str:
    return "{app_label}/{model_name}/{id}/{filename}".format(
        app_label=instance._meta.app_label,
        model_name=instance._meta.model_name,
        id=instance.id,
        filename=filename,
    )


class VCFMixin(models.Model):
    class Meta:
        abstract = True

    vcf_file = models.FileField(
        blank=True,
        max_length=URLFIELD_MAX_LENGTH,
        upload_to=vcf_file_path,
        storage=MediaStorage(),
        validators=[FileExtensionValidator(["vcf"])],
        verbose_name=_("VCF file"),
    )
