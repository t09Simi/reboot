from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        CAREER_GAPER = 'career_gaper', 'Career Gaper'
        MENTOR = 'mentor', 'Mentor'

    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CAREER_GAPER
    )
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.email


class CareerGapProfile(models.Model):
    class EmploymentStatus(models.TextChoices):
        EMPLOYED = 'employed', 'Employed'
        UNEMPLOYED = 'unemployed', 'Unemployed'
        FREELANCING = 'freelancing', 'Freelancing'
        STUDYING = 'studying', 'Studying'


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employment_status = models.CharField(
        max_length=20,
        choices = EmploymentStatus.choices,
        default=EmploymentStatus.UNEMPLOYED)
    education = models.CharField(max_length=50)
    prior_experience = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    portfolio = models.URLField(blank=True)
    interests = models.CharField(max_length=50, blank=True)
    gap_story = models.TextField(blank=True)
    gap_duration= models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.name}'s Profile"
    

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.CharField(max_length=50,blank=True)
    skills = models.TextField(blank=True)
    company = models.CharField(max_length=100,blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    portfolio = models.URLField(blank=True)
    interests = models.CharField(max_length=200, blank=True)
    availability = models.BooleanField(default=True)
    availability_times = models.CharField(
    max_length=200, 
    blank=True,
    help_text="e.g. Weekends 10am-12pm IST"
)


    def __str__(self):
        return f"{self.user.name}'s Profile"