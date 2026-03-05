from django.db import models
from django.conf import settings

class Domain(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, blank=True)  # emoji icon
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class JobRole(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    domain = models.ForeignKey(
    Domain,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='job_roles')
    created_by = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class SkillCategory(models.Model):
    name = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Skill(models.Model):
    class SkillImportance(models.TextChoices):
        REQUIRED = 'required', 'Required'
        PREFERRED = 'preferred', 'Preferred'
        BONUS = 'bonus', 'Bonus'

    name = models.CharField(max_length=300)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE,related_name='category_skills')
    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name='role_skills')
    importance = models.CharField(
        max_length=20,
        choices=SkillImportance.choices,
        default=SkillImportance.REQUIRED
    )

    def __str__(self):
        return f"{self.name} ({self.category})"
    