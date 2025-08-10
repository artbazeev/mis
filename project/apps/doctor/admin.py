from apps.doctor.models import Doctor
from django.contrib import admin


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass
