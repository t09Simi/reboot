from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    context = {}

    if request.user.role == 'career_gaper':
        context['profile'] = request.user.careergapprofile

    elif request.user.role == 'mentor':
        # Get career gapers who have started filling their profile
        context['career_gapers'] = User.objects.filter(role = 'career_gaper')

    return render(request, 'core/dashboard.html', context)
