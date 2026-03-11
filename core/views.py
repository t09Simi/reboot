from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from mentorship.models import MentorshipRequest

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    context = {}

    if request.user.role == 'career_gaper':

        context['profile'] = request.user.careergapprofile

        context['my_requests'] = MentorshipRequest.objects.filter(
        sender=request.user).select_related('receiver', 'receiver__mentorprofile').order_by('-created_at')

    elif request.user.role == 'mentor':
        # Get career gapers requests 
        context['received_requests'] = MentorshipRequest.objects.filter(
        receiver=request.user,
        status='pending').select_related('sender', 'sender__careergapprofile')

    return render(request, 'core/dashboard.html', context)
