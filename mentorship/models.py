from django.db import models
from django.conf import settings

# Create your models here.
class MentorshipRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'
        SESSION_BOOKED = 'session_booked', 'Session Booked'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_requests')
    
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_requests')

    status = models.CharField(
        max_length=50,
        choices = Status.choices,
        default= Status.PENDING
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name} sent request to {self.receiver.name}"
    
class Session(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions_as_mentor')
    
    career_gaper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions_as_gaper')
    
    request = models.ForeignKey(
        MentorshipRequest,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    
    scheduled_at = models.DateTimeField()

    duration = models.IntegerField(default=30)

    meeting_link = models.CharField(max_length=500, blank=True)

    status = models.CharField(
        max_length=50,
        choices = Status.choices,
        default= Status.SCHEDULED
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.career_gaper} session with {self.mentor} - {self.status}"

    class Meta:
        ordering = ['scheduled_at']
        