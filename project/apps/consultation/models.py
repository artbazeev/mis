from typing import Final

from django.db import models

from apps.doctor.models import Doctor
from apps.helpers.models import CreatedModel, UUIDModel, enum_max_length
from apps.patient.models import Patient

_FIELD_MAX_LENGTH: Final = 150


class StatusChoices(models.TextChoices):
    WAITING = "waiting", "Ожидает"
    CONFIRMED = "confirmed", "Подтверждена"
    STARTED = "started", "Начата"
    COMPLETED = "completed", "Завершена"
    PAID = "paid", "Оплачена"


class Consultation(UUIDModel, CreatedModel):
    start_time = models.DateTimeField("Время начала консультации")
    end_time = models.DateTimeField("Время конца консультации")
    status = models.CharField(
        "Статус консультации",
        max_length=enum_max_length(StatusChoices),
        choices=StatusChoices.choices,
        default=StatusChoices.WAITING,
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="consultations"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="consultations"
    )
    result = models.TextField(
        "Результат консультации/Описание болезни или диагноза", blank=True
    )

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"

    def __str__(self):
        return f"Консультация {self.id} - {self.doctor} с пациентом: {self.patient}"
