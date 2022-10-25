import os

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VEPConfig(AppConfig):
    ENSEMBL_VEP_VERSION = str(os.environ.get("ENSEMBL_VEP_VERSION", ""))

    name = "vep"
    verbose_name = _("Ensembl VEP app")
