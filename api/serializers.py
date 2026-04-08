from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from accounts.models import User

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

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
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
        
        