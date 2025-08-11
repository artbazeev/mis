from rest_framework import serializers

from api.v1.clinic.serializers import ClinicReadSerializer
from apps.doctor.models import Doctor
from apps.helpers.serializers import EagerLoadingSerializerMixin


class DoctorReadSerializer(EagerLoadingSerializerMixin, serializers.ModelSerializer):
    last_name = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    patronymic = serializers.SerializerMethodField()
    clinics = ClinicReadSerializer(many=True, read_only=True)

    prefetch_related_fields = [
        "clinics",
    ]

    class Meta:
        model = Doctor
        fields = (
            "id",
            "last_name",
            "first_name",
            "patronymic",
            "specialization",
            "clinics",
        )

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_patronymic(self, obj):
        return obj.user.patronymic


class DoctorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id", "user", "specialization", "clinics")
