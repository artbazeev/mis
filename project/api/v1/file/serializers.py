from apps.file.models import File
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)  # noqa: WPS110

    class Meta:
        model = File
        fields = (
            "id",
            "file",
        )

        read_only_fields = ("id",)
