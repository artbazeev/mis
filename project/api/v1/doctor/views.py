from apps.helpers.viewsets import CRUDExtendedModelViewSet
from apps.doctor.models import Doctor
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from .serializers import DoctorReadSerializer


class DoctorViewSet(CRUDExtendedModelViewSet):

    queryset = Doctor.objects.all()
    serializer_class = DoctorReadSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # filterset_class =
    # serializer_class_map = {
    #
    # }
    permission_classes = (permissions.IsAuthenticated,)

