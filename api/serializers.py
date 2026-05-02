from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from accounts.models import User, CareerGapProfile, MentorProfile
from mentorship.models import MentorshipRequest

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                'No active account found with the given credentials'
            )

        refresh = self.get_token(user)

        refresh['role'] = user.role
        refresh['name'] = user.name

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role':user.role,
            'name': user.name,
        }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['name','email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
        username=validated_data['email'],  # use email as username
        email=validated_data['email'],
        name=validated_data['name'],
        password=validated_data['password'],
        role=validated_data['role']
        )
        return user
    
class CareerGaperProfileSerializer(serializers.ModelSerializer):
    # feilds from User model
    name = serializers.CharField(source='user.name', read_only = True)
    email = serializers.CharField(source = 'user.email', read_only = True)

    class Meta:
        model = CareerGapProfile
        fields = [
            'name', 'email',
            'employment_status', 'education',
            'prior_experience', 'certifications',
            'projects', 'portfolio',
            'interests', 'gap_story',
            'gap_duration', 'profile_picture'
        ]
        extra_kwargs = {
            'employment_status': {'required': False},
            'education': {'required': False},
            'prior_experience': {'required': False},
            'certifications': {'required': False},
            'projects': {'required': False},
            'portfolio': {'required': False},
            'interests': {'required': False},
            'gap_story': {'required': False},
            'gap_duration': {'required': False},
            'profile_picture': {'required': False},
        }
 
class MentorProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only = True)
    email = serializers.CharField(source = 'user.email', read_only = True)
        
    class Meta:
        model = MentorProfile
        fields = [
            'name', 'email',
            'education', 'skills',
            'company', 'years_of_experience',
            'portfolio', 'interests',
            'availability', 'availability_times'
        ]
        extra_kwargs = {
            'education' : {'required': False},
            'skills' : {'required': False},
            'company': {'required': False},
            'years_of_experience' : {'required': False},
            'portfolio' : {'required': False},
            'availability' : {'required': False},
            'availability_times' : {'required': False},
        }

class MentorListSerializer(serializers.ModelSerializer):
    mentorprofile = MentorProfileSerializer(read_only = True)

    class Meta:
        model = User
        fields = ['id', 'name', 'mentorprofile']

class MentorshipRequestSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only = True)
    receiver_name = serializers.CharField(source='receiver.name', read_only = True)
    class Meta:
        model = MentorshipRequest
        fields = ['id', 'sender_name', 'receiver_name', 'status', 'message', 'created_at']

        