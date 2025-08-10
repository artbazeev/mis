import pathlib
from secrets import token_urlsafe

from apps.helpers.models import CreatedModel, DeletedModel, UUIDModel
from django.db import models
from django.utils import timezone


def directory_path(instance, filename):
    date = timezone.now().strftime("%Y/%m/%d")
    random_string = token_urlsafe(10)
    extension = pathlib.Path(filename).suffix
    return f"upload/{date}/{random_string}{extension}"


class File(UUIDModel, CreatedModel, DeletedModel):  # noqa: WPS110
    file = models.FileField(upload_to=directory_path)  # noqa: WPS110

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.file.url
