from typing import Final

from django.db import models

from apps.clinic.models import Clinic
from apps.helpers.models import CreatedModel, UUIDModel
from apps.user.models import User

_FIELD_MAX_LENGTH: Final = 150


class Doctor(UUIDModel, CreatedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialization = models.CharField("Специализация", max_length=_FIELD_MAX_LENGTH)
    clinics = models.ManyToManyField(
        Clinic,
        verbose_name="Клиники, в которых работает доктор",
        related_name="doctors",
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Доктор"
        verbose_name_plural = "Доктора"

    def __str__(self):
        return f"{self.user}"
