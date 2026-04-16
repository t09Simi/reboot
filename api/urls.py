from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (RegisterView, CustomTokenObtainPairView, CareerGaperProfileView, MentorProfileView, 
                    MentorListView, MentorDetailView, SendRequestView, MyRequestView ,
                    ReceivedRequestView, RespondRequestView)

#app_name = 'api'

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('career-gaper/profile/', CareerGaperProfileView.as_view(), name='career_gaper_profile'),
    path('mentor/profile/', MentorProfileView.as_view(), name='mentor_profile'),
    path('mentors/', MentorListView.as_view(), name='mentor_list'),
    path('mentors/<int:pk>/', MentorDetailView.as_view(), name='mentor_detail'),
    path('requests/send/<int:pk>/', SendRequestView.as_view(), name='send_request'),
    path('requests/mine/', MyRequestView.as_view(), name='my_requests'),
    path('requests/received/', ReceivedRequestView.as_view(), name='received_requests'),
    path('requests/<int:pk>/respond/', RespondRequestView.as_view(), name='respond_request'),
]