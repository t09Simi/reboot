from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Notification
# Create your views here.

@login_required
def mark_read(request, pk):
    instance = get_object_or_404(Notification, pk=pk, recipient=request.user)
    instance.is_read = True
    instance.save()
    return redirect(instance.link)

@login_required
def mark_all_read(request):
    instance = Notification.objects.filter(
        recipient = request.user,
        is_read = False
    ).update(is_read = True)
    return redirect('core:dashboard')