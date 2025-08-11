from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.doctor.models import Doctor
from apps.helpers.permissions import DoctorReadDoctorOrAdminWriteAdminOnly
from apps.helpers.viewsets import CRUDExtendedModelViewSet

from .serializers import DoctorReadSerializer, DoctorWriteSerializer


class DoctorViewSet(CRUDExtendedModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorReadSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    serializer_class_map = {
        "create": DoctorWriteSerializer,
        "update": DoctorWriteSerializer,
        "retrieve": DoctorReadSerializer,
        "list": DoctorReadSerializer,
        "partial_update": DoctorWriteSerializer,
    }
    permission_classes = (
        permissions.IsAuthenticated,
        DoctorReadDoctorOrAdminWriteAdminOnly,
    )
