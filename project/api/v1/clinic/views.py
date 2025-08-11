from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.v1.clinic.serializers import ClinicReadSerializer, ClinicWriteSerializer
from apps.clinic.models import Clinic
from apps.helpers.permissions import ActionPermissionMixin, IsAdmin


class ClinicViewSet(ActionPermissionMixin, viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicReadSerializer

    serializer_class_map = {
        "create": ClinicWriteSerializer,
        "update": ClinicWriteSerializer,
        "retrieve": ClinicReadSerializer,
        "list": ClinicReadSerializer,
        "partial_update": ClinicWriteSerializer,
    }

    action_permissions_map = {
        "list": (AllowAny,),
        "retrieve": (AllowAny,),
        "create": (IsAuthenticated, IsAdmin),
        "update": (IsAuthenticated, IsAdmin),
        "partial_update": (IsAuthenticated, IsAdmin),
        "destroy": (IsAuthenticated, IsAdmin),
    }
