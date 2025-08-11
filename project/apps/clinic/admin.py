from django.contrib import admin

from apps.clinic.models import Clinic


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    pass
