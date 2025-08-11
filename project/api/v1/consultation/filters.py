from django.db.models import Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet

from apps.consultation.models import Consultation


class ConsultationFilter(FilterSet):
    """
    Фильтрация консультаций по ФИО врача/пациента и статусу.
    Параметры запроса:
      - ?doctor_name=Иванов
      - ?patient_name=Мария Сергеевна
      - ?status=confirmed
    """

    doctor_name = filters.CharFilter(method="filter_doctor_name", label="ФИО доктора")
    patient_name = filters.CharFilter(
        method="filter_patient_name", label="ФИО пациента"
    )
    status = filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = Consultation
        fields = ["doctor_name", "patient_name", "status"]

    def filter_doctor_name(self, queryset, name, value):
        if not value:
            return queryset
        parts = [p for p in value.split() if p]
        q = Q()
        for p in parts:
            q |= (
                Q(doctor__user__last_name__icontains=p)
                | Q(doctor__user__first_name__icontains=p)
                | Q(doctor__user__patronymic__icontains=p)
            )
        return queryset.filter(q).distinct()

    def filter_patient_name(self, queryset, name, value):
        if not value:
            return queryset
        parts = [p for p in value.split() if p]
        q = Q()
        for p in parts:
            q |= (
                Q(patient__user__last_name__icontains=p)
                | Q(patient__user__first_name__icontains=p)
                | Q(patient__user__patronymic__icontains=p)
            )
        return queryset.filter(q).distinct()
