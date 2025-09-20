from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Import the new models and serializers
from .models import Profile, DoctorProfile, PatientProfile, PatientDoctorMapping
from .serializers import (
    UserSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
    PatientDoctorMappingSerializer,
)
# Import the new custom permissions from your permissions.py file
from .permissions import IsDoctorUser, IsPatientUser, IsAdminUser

# --- REGISTRATION VIEWS ---
class PatientRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Force the role to 'patient' for this registration endpoint
        request.data['profile'] = {'role': 'patient'}
        # Create the User and Profile
        response = super().create(request, *args, **kwargs)
        # Create the specific PatientProfile linked to the new User
        user = User.objects.get(id=response.data['id'])
        PatientProfile.objects.create(user=user)
        return response

class DoctorRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Force the role to 'doctor' for this registration endpoint
        request.data['profile'] = {'role': 'doctor'}
        # Create the User and Profile
        response = super().create(request, *args, **kwargs)
        # Create the specific DoctorProfile linked to the new User
        user = User.objects.get(id=response.data['id'])
        DoctorProfile.objects.create(user=user)
        return response

# --- PROFILE MANAGEMENT VIEWS ---

# View for a Doctor to manage ONLY their own profile
class DoctorProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctorUser]
    serializer_class = DoctorProfileSerializer
    def get_queryset(self):
        return DoctorProfile.objects.filter(user=self.request.user)

# View for a Patient to manage ONLY their own profile
class PatientProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPatientUser]
    serializer_class = PatientProfileSerializer
    def get_queryset(self):
        return PatientProfile.objects.filter(user=self.request.user)

# --- DOCTOR-SPECIFIC VIEWS ---

# View for a Doctor to see a list of ALL patients in the system
class PatientListViewForDoctors(generics.ListAPIView):
    permission_classes = [IsDoctorUser]
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer

# View for a Doctor to see a list of ONLY the patients assigned to them
class MyAssignedPatientsView(APIView):
    permission_classes = [IsDoctorUser]
    def get(self, request, *args, **kwargs):
        mappings = PatientDoctorMapping.objects.filter(doctor=request.user)
        # Add a check to ensure the patient profile exists before accessing it
        patient_profiles = [mapping.patient.patient_profile for mapping in mappings if hasattr(mapping.patient, 'patient_profile')]
        serializer = PatientProfileSerializer(patient_profiles, many=True)
        return Response(serializer.data)

# --- PATIENT-SPECIFIC VIEWS ---

# View for a logged-in Patient to see their assigned Doctors
class MyAssignedDoctorsView(APIView):
    permission_classes = [IsPatientUser]
    def get(self, request, *args, **kwargs):
        mappings = PatientDoctorMapping.objects.filter(patient=request.user)
        # Add a check to ensure the doctor profile exists before accessing it
        doctor_profiles = [mapping.doctor.doctor_profile for mapping in mappings if hasattr(mapping.doctor, 'doctor_profile')]
        serializer = DoctorProfileSerializer(doctor_profiles, many=True)
        return Response(serializer.data)

# --- MAPPING VIEW (for Admins/Staff) ---

# View for an Admin to assign any patient to any doctor
class AdminAssignPatientToDoctorView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')
        doctor_id = request.data.get('doctor_id')

        try:
            patient = User.objects.get(id=patient_id, profile__role='patient')
            doctor = User.objects.get(id=doctor_id, profile__role='doctor')
        except User.DoesNotExist:
            return Response({"detail": "Patient or Doctor user not found."}, status=status.HTTP_404_NOT_FOUND)
        
        mapping, created = PatientDoctorMapping.objects.get_or_create(patient=patient, doctor=doctor)
        if not created:
            return Response({"detail": "This patient is already assigned to this doctor."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PatientDoctorMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

