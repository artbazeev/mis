from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from api.v1.patient.serializers import PatientReadSerializer, PatientWriteSerializer
from apps.helpers.permissions import IsSelfPatientProfile
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.patient.models import Patient
from apps.user.models import RoleChoices


class PatientViewSet(ExtendedModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientReadSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    serializer_class_map = {
        "create": PatientWriteSerializer,
        "update": PatientWriteSerializer,
        "retrieve": PatientReadSerializer,
        "list": PatientReadSerializer,
        "partial_update": PatientWriteSerializer,
    }
    permission_classes = [IsAuthenticated, IsSelfPatientProfile]

    def get_queryset(self):
        user = self.request.user
        if user.role in (RoleChoices.SUPERUSER, RoleChoices.DOCTOR):
            # врач и суперпользователь видят всех пациентов
            return self.queryset
        if user.role == RoleChoices.PATIENT:
            # пациент видит только себя (по связке Patient.user)
            return self.queryset.filter(user=user)
        return self.queryset.none()
