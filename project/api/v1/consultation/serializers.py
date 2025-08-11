from rest_framework import serializers

from api.v1.doctor.serializers import DoctorReadSerializer
from api.v1.patient.serializers import PatientReadSerializer
from apps.consultation.models import Consultation
from apps.helpers.serializers import EagerLoadingSerializerMixin


class ConsultationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ("status",)


class ConsultationReadSerializer(
    EagerLoadingSerializerMixin, serializers.ModelSerializer
):
    doctor = DoctorReadSerializer()
    patient = PatientReadSerializer()
    select_related_fields = [
        "doctor",
        "patient",
    ]

    class Meta:
        model = Consultation
        fields = [
            "id",
            "created_at",
            "start_time",
            "end_time",
            "status",
            "doctor",
            "patient",
            "result",
        ]


class ConsultationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = [
            "id",
            "created_at",
            "start_time",
            "end_time",
            "status",
            "doctor",
            "patient",
        ]

    def validate(self, data):
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError(
                "Дата начала консультации должно быть раньше чем конец консультации."
            )
        return data
