from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import User
from .models import MentorshipRequest

@login_required
def mentor_list(request):
    mentors = User.objects.filter(role="mentor").select_related('mentorprofile').order_by('-mentorprofile__availability')
    return render(request, 'mentorship/mentor_list.html', {'mentors': mentors})

@login_required
def mentor_profile(request, pk):
    mentor = get_object_or_404(User, pk=pk, role='mentor')

    existing_request = MentorshipRequest.objects.filter(sender=request.user,
        status__in=['pending', 'accepted', 'session_booked']
    ).first()

    can_send_request = not existing_request
    return render(request, 'mentorship/mentor_profile.html', {
        'mentor': mentor,
        'can_send_request': can_send_request,
        'existing_request': existing_request,
    })

@login_required
def send_request(request, pk):
    mentor = get_object_or_404(User, pk=pk, role='mentor')
    
    if request.method == 'POST':
        message = request.POST.get('message')
        
        MentorshipRequest.objects.create(
            sender=request.user,
            receiver=mentor,
            message=message,
            status='pending'
        )
        messages.success(request, f"🎉 Your request has been sent to {mentor.name}!")
        return redirect('mentorship:mentor_profile', pk=pk)
    
    return redirect('mentorship:mentor_profile', pk=pk)

@login_required
def respond_request(request, pk):
    instance = get_object_or_404(MentorshipRequest, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
            instance.status = 'accepted'
            instance.save()
            messages.success(request, f"You accepted {instance.sender.name}'s request! ")    
        
        elif action == 'decline':
            instance.status = 'declined'
            instance.save()
            messages.success(request, f"You declined {instance.sender.name}'s request! ")

        return redirect('core:dashboard')


