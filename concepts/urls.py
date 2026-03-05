from django.urls import path
from .import views

app_name = 'concepts'

urlpatterns = [
    path('', views.job_roles_list, name ='job_roles_list'),
    path('<int:pk>/', views.job_role_detail, name='job_role_detail'),
]
