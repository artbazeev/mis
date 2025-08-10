from apps.file.models import File
from django.contrib import admin


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass  # noqa: WPS420 WPS604
