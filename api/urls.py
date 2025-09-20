from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    PatientRegisterView,
    DoctorRegisterView,
    DoctorProfileViewSet,
    PatientProfileViewSet,
    PatientListViewForDoctors,
    MyAssignedPatientsView,
    MyAssignedDoctorsView,
    AdminAssignPatientToDoctorView,
)

# The router will handle the ViewSets for self-profile management.
# This will create URLs like:
# /api/doctor-profile/ for listing and creating (for the logged-in doctor)
# /api/doctor-profile/{id}/ for retrieving, updating, and deleting
# /api/patient-profile/ (and with {id})
router = DefaultRouter()
router.register(r'doctor-profile', DoctorProfileViewSet, basename='doctor-profile')
router.register(r'patient-profile', PatientProfileViewSet, basename='patient-profile')

urlpatterns = [
    # --- Authentication and Registration ---
    path('auth/register/patient/', PatientRegisterView.as_view(), name='register-patient'),
    path('auth/register/doctor/', DoctorRegisterView.as_view(), name='register-doctor'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'), # A single login for all roles

    # --- API Endpoints ---
    # Doctor-specific routes
    path('doctors/all-patients/', PatientListViewForDoctors.as_view(), name='all-patients-for-doctors'),
    path('doctors/my-patients/', MyAssignedPatientsView.as_view(), name='my-assigned-patients'),
    
    # Patient-specific routes
    path('patients/my-doctors/', MyAssignedDoctorsView.as_view(), name='my-assigned-doctors'),

    # Admin-specific routes
    path('admin/assign-patient/', AdminAssignPatientToDoctorView.as_view(), name='admin-assign-patient'),

    # Include the router-generated URLs for self-profile management
    path('', include(router.urls)),
]

