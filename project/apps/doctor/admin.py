from django.contrib import admin

from apps.doctor.models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass
