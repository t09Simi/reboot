from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, CustomTokenObtainPairView, CareerGaperProfileView, MentorProfileView, MentorListView, MentorDetailView

#app_name = 'api'

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('career-gaper/profile/', CareerGaperProfileView.as_view(), name='career_gaper_profile'),
    path('mentor/profile/', MentorProfileView.as_view(), name='mentor_profile'),
    path('mentors/', MentorListView.as_view(), name='mentor_list'),
    path('mentors/<int:pk>/', MentorDetailView.as_view(), name='mentor_detail'),

]