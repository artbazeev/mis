from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated

from apps.user.models import RoleChoices


class IsAdmin(BasePermission):
    """
    Полные права на все действия.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == RoleChoices.SUPERUSER
        )


def _is_doctor(user):
    role = getattr(user, "role", None)
    return role == RoleChoices.DOCTOR


class IsConsultationOwnerDoctor(BasePermission):
    """
    Врач может работать только со своими консультациями.
    Работает даже если у пользователя несколько докторских профилей.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if getattr(view, "action", None) == "create":
            return user.is_staff or user.is_superuser or _is_doctor(user)

        # Остальные действия решим на объектном уровне (если надо)
        return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role != RoleChoices.DOCTOR:
            return False
        # Проверяем, что доктор из Consultation связан с этим пользователем
        return request.user.doctor_profile.filter(id=obj.doctor_id).exists()


class IsConsultationOwnerPatient(BasePermission):
    """
    Пациент видит только свои консультации.
    Если у пациента несколько профилей — проверяет все.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user.role != RoleChoices.PATIENT:
            return False
        return request.user.patient_profile.filter(id=obj.patient_id).exists()


class IsConsultationParticipant(BasePermission):
    """
    Доступ имеют только участники консультации — либо врач,
    либо пациент этой консультации.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.role == RoleChoices.DOCTOR:
            return request.user.doctor_profile.filter(id=obj.doctor_id).exists()

        if request.user.role == RoleChoices.PATIENT:
            return request.user.patient_profile.filter(id=obj.patient_id).exists()

        return False


class IsSelfPatientProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in (RoleChoices.SUPERUSER, RoleChoices.DOCTOR):
            return True
        return (
            request.user.role == RoleChoices.PATIENT and obj.user_id == request.user.id
        )


def _role_value(user):
    role = getattr(user, "role", None)
    return role.value if hasattr(role, "value") else role


class IsDoctorOrAdminForCreate(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(view, "action", None) != "create":
            return True
        role = _role_value(request.user)
        return (
            request.user.is_superuser
            or request.user.is_staff
            or role == RoleChoices.DOCTOR
        )


def role_value(user):
    role = getattr(user, "role", None)
    return getattr(role, "value", role)  # поддержка Enum и строки


class DoctorReadDoctorOrAdminWriteAdminOnly(BasePermission):
    def has_permission(self, request, view):
        u = getattr(request, "user", None)
        if not (u and u.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            # список/получение — доктор или админ
            return u.is_staff or u.is_superuser or role_value(u) == RoleChoices.DOCTOR
        # создание/изменение/удаление — только админ
        return u.is_staff or u.is_superuser


class ActionPermissionMixin:
    """
    Позволяет задать словарь: action -> tuple(permission classes).
    Для неуказанных action берётся default_permissions.
    """

    default_permissions = (IsAuthenticated,)
    action_permissions_map = {}

    def get_permissions(self):
        classes = self.action_permissions_map.get(self.action, self.default_permissions)
        return [cls() for cls in classes]
