
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Patient, Doctor, PatientDoctorMapping

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        source="first_name",
        max_length=150
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered."
            )

        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data["email"]

        return User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=validated_data["first_name"],
        )


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id", "name", "age", "gender", "email",
            "address", "created_by", "created_at"
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_age(self, value):
        if value > 130:
            raise serializers.ValidationError(
                "Age cannot exceed 130."
            )
        return value

    def validate_gender(self, value):
        if value.lower() not in ["male", "female", "other"]:
            raise serializers.ValidationError(
                "Gender must be Male, Female, or Other."
            )
        return value


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id", "name", "specialization", "email",
            "phone", "created_by", "created_at"
        ]
        read_only_fields = ["id", "created_by", "created_at"]


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(
        source="doctor.name", read_only=True
    )
    doctor_specialization = serializers.CharField(
        source="doctor.specialization", read_only=True
    )

    class Meta:
        model = PatientDoctorMapping
        fields = [
            "id", "patient", "doctor", "doctor_name",
            "doctor_specialization", "assigned_at"
        ]
        read_only_fields = ["id", "assigned_at"]

    def validate(self, attrs):
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")
        user = self.context["request"].user

        if not Patient.objects.filter(
            pk=patient.pk, created_by=user
        ).exists():
            raise serializers.ValidationError({
                "patient": "Patient not found or not accessible."
            })

        if PatientDoctorMapping.objects.filter(
            patient=patient, doctor=doctor
        ).exists():
            raise serializers.ValidationError(
                "This doctor is already assigned to this patient."
            )

        return attrs
