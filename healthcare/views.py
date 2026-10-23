
from django.contrib.auth import authenticate, get_user_model

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    RegisterSerializer,
    PatientSerializer,
    DoctorSerializer,
    PatientDoctorMappingSerializer,
)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        if not isinstance(email, str) or not isinstance(password, str):
            return Response(
                {"error": "Email and password must be strings."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = email.strip().lower()

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is None:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(
            created_by=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        return Doctor.objects.all().order_by("name")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        ).select_related("patient", "doctor")

    def perform_create(self, serializer):
        serializer.save()


class PatientMappingsView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]

        patient = Patient.objects.filter(
            id=patient_id,
            created_by=self.request.user,
        ).first()

        if patient is None:
            raise NotFound("Patient not found.")

        return PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related("patient", "doctor")


class MappingDeleteView(generics.DestroyAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user
        )

class MappingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        patient = Patient.objects.filter(
            id=pk,
            created_by=request.user
        ).first()

        if patient is None:
            raise NotFound("Patient not found.")

        mappings = PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related("patient", "doctor")

        serializer = PatientDoctorMappingSerializer(
            mappings, many=True
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = PatientDoctorMapping.objects.filter(
            id=pk,
            patient__created_by=request.user
        ).first()

        if mapping is None:
            raise NotFound("Mapping not found.")

        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
