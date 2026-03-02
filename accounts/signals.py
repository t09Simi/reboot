from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CareerGapProfile, MentorProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.CAREER_GAPER:
            CareerGapProfile.objects.create(user=instance)
        elif instance.role == User.Role.MENTOR:
            MentorProfile.objects.create(user=instance)