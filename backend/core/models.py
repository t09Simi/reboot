from django.db import models
from django.conf import settings

# Create your models here.
class Testimonial(models.Model):
    class ApprovalStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        MENTOR_APPROVED = 'mentor_approved', 'Mentor_Approved'
        PUBLISHED = 'published' , 'Published'

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='testimonials_written'
        )
    
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='testimonials_confirmed',
        null=True,
        blank=True
    )

    message = models.TextField()
    profile_picture = models.ImageField(upload_to='testimonials/',
        blank=True,
        null=True)
    designation = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=50,
        choices = ApprovalStatus.choices,
        default= ApprovalStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.name}'s Testimonial"