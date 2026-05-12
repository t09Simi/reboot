from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from accounts.models import CareerGapProfile, MentorProfile, User
from mentorship.models import MentorshipRequest
from notifications.models import Notification
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, CareerGaperProfileSerializer, MentorProfileSerializer, MentorListSerializer, MentorshipRequestSerializer
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

class MentorListView(APIView):
    def get(self, request):
        mentors = User.objects.filter(role='mentor').select_related('mentorprofile').order_by('-mentorprofile__availability')
        serializer = MentorListSerializer(mentors, many=True)
        return Response(serializer.data)
    

class MentorDetailView(APIView):
    def get(self, request, pk):
        mentor = get_object_or_404(User, pk=pk, role='mentor')
        serializer = MentorListSerializer(mentor)
        return Response(serializer.data)
    
#POST /api/requests/send/<mentor_pk>/  → send request
#GET  /api/requests/mine/              → career gaper's requests
#GET  /api/requests/received/          → mentor's received requests
#POST /api/requests/<pk>/respond/      → accept or decline

class SendRequestView(APIView):
    def post(self, request, pk):
        mentor = get_object_or_404(User, pk=pk, role='mentor')
        message = request.data.get('message')

        if not message:
            return Response(
                {'error': 'Message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        mentorship_request = MentorshipRequest.objects.create(
            sender=request.user,
            receiver=mentor,
            message=message,
            status='pending'
        )

        Notification.objects.create(
            recipient=mentor,
            message=f"{request.user.name} sent you a mentorship request!",
            link="/dashboard/"
        )

        serializer = MentorshipRequestSerializer(mentorship_request)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    
class MyRequestView(APIView):
    def get(self, request):
        requests = MentorshipRequest.objects.filter(sender=request.user)
        serializer = MentorshipRequestSerializer(requests, many=True)
        return Response(serializer.data)
    

class ReceivedRequestView(APIView):
    def get(self, request):
        requests = MentorshipRequest.objects.filter(receiver=request.user)
        serializer = MentorshipRequestSerializer(requests, many=True)
        return Response(serializer.data)

class RespondRequestView(APIView):
    def post(self, request, pk):
        instance = get_object_or_404(MentorshipRequest, pk=pk)
        action = request.data.get('action') 

        if action == 'accept':
            instance.status = 'accepted'
            instance.save()

            Notification.objects.create(
                recipient = instance.sender,
                message = f"{instance.receiver.name} accepted your mentorship request! 🎉",
                link = "/dashboard/"
            )

        elif action == 'decline':
            instance.status = 'declined'
            instance.save()

            Notification.objects.create(
                recipient = instance.sender,
                message = f"{instance.receiver.name} declined your mentorship request.",
                link = "/dashboard/"
            )

        serializer = MentorshipRequestSerializer(instance)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
