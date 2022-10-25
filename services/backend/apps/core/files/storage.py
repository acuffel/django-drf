import os
from pathlib import Path

from django.core.files.storage import FileSystemStorage
from django.conf import settings


def get_filename_with_suffix(filename: str, suffix: str) -> str:
    """
    Adds a suffix to a filename before the extension.
    Example:
        >>> get_filename_with_suffix(
                filename="foo/bar.txt",
                suffix="baz",
            )
        'foo/bar_baz.txt'
    """
    input_path: Path = Path(filename)
    output_filename: str = input_path.stem + "_" + suffix + input_path.suffix
    output_path: Path = input_path.parent / output_filename
    return str(output_path)


class MediaStorage(FileSystemStorage):
    location = settings.MEDIA_ROOT
    base_url = settings.MEDIA_URL

    def get_available_name(self, name, max_length=None):
        """Removes any previously stored file (if any) before returning the name."""
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name


class BiodbStorage(MediaStorage):
    location = settings.BIODB_ROOT
    base_url = settings.BIODB_URL
