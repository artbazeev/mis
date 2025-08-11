from typing import Final

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import CreatedModel, UUIDModel
from apps.user.models import User

_FIELD_MAX_LENGTH: Final = 150


class Patient(UUIDModel, CreatedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    additional_phone = PhoneNumberField(
        "Доп. номер телефона",
        blank=True,
        null=True,
        help_text="Пример, +79510549236",
    )
    additional_email = models.EmailField("Доп. email", blank=True, null=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return f"{self.user}"
