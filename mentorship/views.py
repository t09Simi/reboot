from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import User
from .models import MentorshipRequest, Session
from .forms import SessionForm
from notifications.models import Notification

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
def career_gaper_profile(request, pk):
    career_gaper = get_object_or_404(User, pk=pk, role='career_gaper')

    instance_requested = MentorshipRequest.objects.filter(
        sender = career_gaper,
        receiver = request.user
    ).first()

    return render(request, 'mentorship/career_gaper_profile.html', {
        'career_gaper': career_gaper,
        'profile': career_gaper.careergapprofile,
        'instance_requested': instance_requested
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
        
        # Notify the mentor
        Notification.objects.create(
            recipient=mentor,
            message=f"{request.user.name} sent you a mentorship request!",
            link="/dashboard/"
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

            Notification.objects.create(
                recipient = instance.sender,
                message = f"{instance.receiver.name} accepted your mentorship request! 🎉",
                link = "/dashboard/"
            )
            messages.success(request, f"You accepted {instance.sender.name}'s request! ")    
        
        elif action == 'decline':
            instance.status = 'declined'
            instance.save()

            Notification.objects.create(
                recipient = instance.sender,
                message = f"{instance.receiver.name} declined your mentorship request.",
                link = "/dashboard/"
            )
            messages.success(request, f"You declined {instance.sender.name}'s request! ")
        return redirect('core:dashboard')

#Session booking

@login_required
def schedule_session(request, pk):
    instance = get_object_or_404(MentorshipRequest, pk=pk)

    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.mentor = request.user
            session.career_gaper = instance.sender
            session.request = instance
            session.save()

            # Update request status
            instance.status = 'session_booked'
            instance.save()

            # Notify career gaper
            Notification.objects.create(
                recipient=instance.sender,
                message=f"{request.user.name} scheduled a session with you! 📅",
                link="/dashboard/"
            )
        messages.success(request,f"Session booked with {instance.sender.name}!")
        return redirect('core:dashboard')
    else:
        form = SessionForm()

    return render(request, 'mentorship/schedule_session.html', {
        'form': form,
        'instance': instance
    })
