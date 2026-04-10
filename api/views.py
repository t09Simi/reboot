from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from accounts.models import CareerGapProfile, MentorProfile
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, CareerGaperProfileSerializer, MentorProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message':'Account created successfully!'

                }, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CareerGaperProfileView(APIView):
    def get(self, request):
        profile = get_object_or_404(CareerGapProfile, user=request.user)
        serializer = CareerGaperProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request):
        profile = get_object_or_404(CareerGapProfile, user=request.user)
        serializer =  CareerGaperProfileSerializer(
            profile,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MentorProfileView(APIView):
    def get(self, request):
        profile = get_object_or_404(MentorProfile, user=request.user)
        serializer = MentorProfileSerializer(profile)
        return Response(serializer.data)    
    
    def put(self, request):
        profile = get_object_or_404(MentorProfile, user=request.user)
        serializer = MentorProfileSerializer(
            profile,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)