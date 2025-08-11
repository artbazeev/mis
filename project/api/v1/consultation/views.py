from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.consultation.models import Consultation, StatusChoices
from apps.helpers.permissions import (
    ActionPermissionMixin,
    IsAdmin,
    IsConsultationOwnerDoctor,
    IsConsultationParticipant,
)
from apps.helpers.serializers import EnumSerializer
from apps.helpers.viewsets import ExtendedModelViewSet
from apps.user.models import RoleChoices

from .filters import ConsultationFilter
from .serializers import (
    ConsultationReadSerializer,
    ConsultationStatusSerializer,
    ConsultationWriteSerializer,
)


class ConsultationViewSet(ActionPermissionMixin, ExtendedModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ConsultationFilter
    serializer_class_map = {
        "create": ConsultationWriteSerializer,
        "update": ConsultationWriteSerializer,
        "retrieve": ConsultationReadSerializer,
        "list": ConsultationReadSerializer,
        "partial_update": ConsultationWriteSerializer,
    }

    action_permissions_map = {
        "list": (IsAuthenticated,),
        "retrieve": (IsAuthenticated, IsConsultationParticipant),
        "create": (IsAuthenticated, IsAdmin | IsConsultationOwnerDoctor),
        "update": (IsAuthenticated, IsAdmin | IsConsultationOwnerDoctor),
        "partial_update": (IsAuthenticated, IsAdmin | IsConsultationOwnerDoctor),
        "destroy": (IsAuthenticated, IsAdmin | IsConsultationOwnerDoctor),
        "set_status": (IsAuthenticated, IsAdmin | IsConsultationOwnerDoctor),
    }

    def get_queryset(self):
        user = self.request.user
        qs = self.queryset

        if user.role == RoleChoices.DOCTOR:
            return qs.filter(doctor__user=user)
        if user.role == RoleChoices.PATIENT:
            return qs.filter(patient__user=user)
        if user.role == RoleChoices.SUPERUSER:
            return qs

        return qs.none()

    @swagger_auto_schema(responses={200: EnumSerializer})
    @action(methods=["get"], detail=False)
    def status_types(self, request):
        """Возвращает возможные типы консультаций"""
        return Response(EnumSerializer(StatusChoices, many=True).data)

    @swagger_auto_schema(responses={200: ConsultationReadSerializer})
    @action(
        detail=True, methods=["post"], serializer_class=ConsultationStatusSerializer
    )
    def set_status(self, request, pk=None):
        consultation = self.get_object()
        serializer = ConsultationStatusSerializer(
            consultation, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ConsultationReadSerializer(consultation).data)
