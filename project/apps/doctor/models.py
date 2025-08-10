from typing import Final

from apps.helpers.models import CreatedModel, UUIDModel
from apps.user.admin import User
from django.db import models

_FIELD_MAX_LENGTH: Final = 150


class Doctor(UUIDModel, CreatedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_profile')
    first_name = models.CharField("Отчество", max_length=_FIELD_MAX_LENGTH)
    last_name = models.CharField("Фамилия", max_length=_FIELD_MAX_LENGTH)
    patronymic = models.CharField("Отчество", max_length=_FIELD_MAX_LENGTH, blank=True)
    specialization = models.CharField("Специализация", max_length=_FIELD_MAX_LENGTH)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Доктор"
        verbose_name_plural = "Доктора"

    def __str__(self):
        return f"{self.first_name}"
