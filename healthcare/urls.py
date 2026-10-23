
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    RegisterView,
    LoginView,
    PatientViewSet,
    DoctorViewSet,
    MappingListCreateView,
    MappingDetailView,
)

router = SimpleRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("", include(router.urls)),
    path("mappings/", MappingListCreateView.as_view()),
    path("mappings/<int:pk>/", MappingDetailView.as_view()),
]
