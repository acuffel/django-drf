from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.files.storage import BiodbStorage

URLFIELD_MAX_LENGTH = 2048


def fasta_file_path(instance, filename) -> str:
    """Used only for manual uploads."""
    return "uploads/{app_label}/{model_name}/{id}/fasta/file/{filename}".format(
        app_label=instance._meta.app_label,
        model_name=instance._meta.model_name,
        id=instance.id,
        filename=filename,
    )


def fasta_index_file_path(instance, filename) -> str:
    """Used only for manual uploads."""
    return fasta_file_path(instance, filename)


class FASTAMixin(models.Model):
    fasta_file = models.FileField(
        blank=True,
        max_length=URLFIELD_MAX_LENGTH,
        upload_to=fasta_file_path,
        storage=BiodbStorage(),
        validators=[FileExtensionValidator(["fa"])],
        verbose_name=_("FASTA file"),
    )

    fasta_index_file = models.FileField(
        blank=True,
        max_length=URLFIELD_MAX_LENGTH,
        upload_to=fasta_index_file_path,
        storage=BiodbStorage(),
        validators=[FileExtensionValidator(["fai"])],
        verbose_name=_("FASTA index file"),
    )

    class Meta:
        abstract = True
