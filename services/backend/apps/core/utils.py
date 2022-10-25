
import json
import logging
from pathlib import Path
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

def get_biodb_catalog() -> dict[str, Any]:
    try:
        catalog_path: Path = settings.BIODB_ROOT / "catalog.json"
        with open(catalog_path, mode="r", encoding="utf_8", errors="strict") as file:
            content = file.read()
            catalog = json.loads(content)
            return catalog
    except Exception as e:
        logger.exception(e)
        return {}
