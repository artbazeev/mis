from typing import Final, final

from django.contrib.auth import models as auth_models
from django.db import models
from django_lifecycle import LifecycleModelMixin
from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.managers import CustomFieldUserManager
from apps.helpers.models import UUIDModel, enum_max_length

_FIELD_MAX_LENGTH: Final = 40


class RoleChoices(models.TextChoices):
    SUPERUSER = "superuser", "Суперпользователь"
    DOCTOR = "doctor", "Доктор"
    PATIENT = "patient", "Пациент"


@final
class User(LifecycleModelMixin, UUIDModel, auth_models.AbstractUser):
    first_name = models.CharField("Имя", max_length=_FIELD_MAX_LENGTH, default="")
    last_name = models.CharField("Фамилия", max_length=_FIELD_MAX_LENGTH, default="")
    patronymic = models.CharField("Отчество", max_length=_FIELD_MAX_LENGTH, blank=True)
    phone = PhoneNumberField(
        "Номер телефона", unique=True, help_text="Пример, +79510549236"
    )
    email = models.EmailField("Адрес электронной почты", default="")
    is_active = models.BooleanField(default=True)
    role = models.CharField(
        "Роль пользователя системы",
        max_length=enum_max_length(RoleChoices),
        choices=RoleChoices.choices,
        default=RoleChoices.PATIENT,
    )
    objects = CustomFieldUserManager(username_field_name="phone")  # noqa: WPS110

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    class Meta(auth_models.AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        ordering = ("email",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def get_username(self):
        # for jwt_payload_handler
        return str(self.phone)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = str(self.phone)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name
