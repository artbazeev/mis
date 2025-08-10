from api.v1.file.serializers import FileSerializer
from api.v1.user.serializers import UserReadSerializer
from apps.doctor.models import Doctor
from rest_framework import serializers

class DoctorReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'
