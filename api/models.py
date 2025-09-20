from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- The core Profile model to define User Roles ---
class Profile(models.Model):
    USER_ROLES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'), # Admin/Superuser role
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# --- The NEW Doctor Profile, linked to a User ---
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, blank=True)
    qualifications = models.TextField(blank=True)
    clinic_address = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

# --- The NEW Patient Profile, linked to a User ---
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    contact_info = models.CharField(max_length=100, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}"

# --- The Mapping Model, now linking two Users ---
class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_assignments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_assignments')

    class Meta:
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"Patient: {self.patient.username} -> Doctor: {self.doctor.username}"

# --- Signals to automatically create Profiles ---
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    # This check is important to prevent errors during initial user creation
    if hasattr(instance, 'profile'):
        instance.profile.save()

