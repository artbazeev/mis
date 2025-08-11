from rest_framework import serializers

from apps.helpers.serializers import EagerLoadingSerializerMixin
from apps.patient.models import Patient


class PatientReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    patronymic = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    select_related_fields = [
        "user",
    ]

    class Meta:
        model = Patient
        fields = [
            "id",
            "last_name",
            "first_name",
            "patronymic",
            "phone",
            "email",
            "additional_phone",
            "additional_email",
        ]

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_patronymic(self, obj):
        return obj.user.patronymic

    def get_phone(self, obj):
        return str(obj.user.phone)

    def get_email(self, obj):
        return obj.user.email


class PatientWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "user",
            "additional_phone",
            "additional_email",
        ]
