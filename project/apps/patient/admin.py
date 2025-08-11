from django.contrib import admin

from apps.patient.models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    pass
