from rest_framework import serializers

from apps.clinic.models import Clinic


class ClinicReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = [
            "id",
            "name",
            "legal_address",
            "physical_address",
        ]


class ClinicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = [
            "id",
            "name",
            "legal_address",
            "physical_address",
        ]
