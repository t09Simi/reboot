from django.urls import path
from . import views

app_name = 'mentorship'

urlpatterns = [
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentors/<int:pk>/', views.mentor_profile, name='mentor_profile'),
    path('mentors/<int:pk>/request/', views.send_request, name='send_request'),
    path('requests/<int:pk>/respond/', views.respond_request, name='respond_request'),
    path('profile/<int:pk>/', views.career_gaper_profile, name='career_gaper_profile'),
]