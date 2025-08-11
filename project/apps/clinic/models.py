from typing import Final

from django.db import models

from apps.helpers.models import CreatedModel, UUIDModel

_FIELD_MAX_LENGTH: Final = 150


class Clinic(UUIDModel, CreatedModel):
    name = models.CharField("Название клиники", max_length=_FIELD_MAX_LENGTH)
    legal_address = models.TextField(
        "Юридический адрес",
    )
    physical_address = models.TextField(
        "Физический адрес",
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Клиника"
        verbose_name_plural = "Клиники"

    def __str__(self):
        return f"{self.name} ({self.physical_address})"
