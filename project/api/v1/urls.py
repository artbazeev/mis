from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from .celery.views import CeleryResultView
from .clinic.views import ClinicViewSet
from .consultation.views import ConsultationViewSet
from .doctor.views import DoctorViewSet
from .patient.views import PatientViewSet
from .user.views import UserViewSet

router = routers.DefaultRouter()
router.register("user", UserViewSet, basename="user")
router.register("clinic", ClinicViewSet, basename="clinic")
router.register("doctor", DoctorViewSet, basename="doctor")
router.register("patient", PatientViewSet, basename="patient")
router.register("consultation", ConsultationViewSet, basename="consultation")
schema_view = get_schema_view(
    openapi.Info(
        title="MIS API",
        default_version="v1",
        description="Простейший сервис МИС",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "swagger(<str:format>.json|.yaml)/",
        schema_view.without_ui(),
        name="schema-json",
    ),
    path("swagger/", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
    path("", include((router.urls, "api-root")), name="api-root"),
    path("celery/result/<pk>/", CeleryResultView.as_view()),
]
