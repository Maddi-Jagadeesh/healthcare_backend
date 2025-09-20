from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile, DoctorProfile, PatientProfile, PatientDoctorMapping

# Serializer for the core Profile model to show the role
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role']

# Serializer for the User model, including the nested Profile
class UserSerializer(serializers.ModelSerializer):
    # This nests the profile data inside the user data
    profile = ProfileSerializer()

    class Meta:
        model = User
        # Include first_name and last_name, as they are important for profiles
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        # Also get first_name and last_name if provided
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )
        
        # Directly access the user's profile, set the role, and save it
        user.profile.role = profile_data['role']
        user.profile.save()
        return user

# Serializer for the Doctor's own profile data
class DoctorProfileSerializer(serializers.ModelSerializer):
    # This makes the user details read-only, showing who this profile belongs to
    user = UserSerializer(read_only=True)
    class Meta:
        model = DoctorProfile
        # The 'id' field is removed for clarity
        fields = ['user', 'specialization', 'qualifications', 'clinic_address']

# Serializer for the Patient's own profile data
class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PatientProfile
        # The 'id' field is removed for clarity
        fields = ['user', 'date_of_birth', 'contact_info', 'medical_history']

# Serializer for the mapping between a Patient user and a Doctor user
class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor']

