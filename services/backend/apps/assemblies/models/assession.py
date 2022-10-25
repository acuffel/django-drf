import os
import logging

from typing import Any

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from assemblies.models import Assembly
from core.models.mixins import MetadataMixin, FASTAMixin

logger = logging.getLogger(__name__)

CHARFIELD_MAX_LENGTH = settings.MY_APP_CHAR_MAX_LENGTH


class Assession(FASTAMixin, MetadataMixin):

    assembly = models.OneToOneField(
        Assembly,
        # If Assembly is deleted, Assession will also be deleted:
        on_delete=models.CASCADE,
        related_name="assessions",
        related_query_name="assession",
        verbose_name=_("assembly"),
    )
    
    name = models.CharField(
        blank=True,
        null=True,
        max_length=CHARFIELD_MAX_LENGTH,
    )

    class Meta(MetadataMixin.Meta):
        verbose_name = _("assession")
        verbose_name_plural = _("assessions")

    def __str__(self):
        return (
            self.name if self.name else _("Assession object ({id})").format(id=self.id)
        )

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.basename(self.fasta_file.name)

        super(Assession, self).save(*args, **kwargs)

    @classmethod
    def load_catalog(cls, catalog: dict[str, Any]) -> None:
        if "assessions" in catalog:
            for assession in catalog["assessions"]:
                try:
                    assembly_id = assession["assembly_id"]
                    name = assession["name"]
                    fasta_file = (
                        assession["fasta_file"] if "fasta_file" in assession else None
                    )
                    fasta_index_file = (
                        assession["fasta_index_file"]
                        if "fasta_index_file" in assession
                        else None
                    )
                except Exception as e:
                    logger.error(e)
                    continue

                # Assembly
                try:
                    assembly_obj = Assembly.objects.get(id=assembly_id)
                except Assembly.DoesNotExist as e:
                    assembly_obj = Assembly.objects.create(id=assembly_id)
                    logger.info("New Assembly: %s", assembly_obj)
                except Exception as e:
                    logger.error(e)
                    continue

                # Assession
                try:
                    assession_obj = cls.objects.get(
                        assembly=assembly_obj,
                        name=name,
                    )
                    logger.warning("Found existing Assession: %s", assession_obj)
                except cls.DoesNotExist as e:
                    assession_obj = cls.objects.create(
                        assembly=assembly_obj,
                        name=name,
                        fasta_file=fasta_file,
                        fasta_index_file=fasta_index_file,
                    )
                    logger.info("New Assession: %s", assession_obj)
                except Exception as e:
                    logger.error(e)
                    continue
