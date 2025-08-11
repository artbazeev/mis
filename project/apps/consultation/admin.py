from django.contrib import admin

from apps.consultation.models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    pass
