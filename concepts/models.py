from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Domain(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, blank=True) 
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class SkillCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Skill Categories'

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    aliases = models.JSONField(
        default=list,
        blank=True,
        help_text="Alternate spellings, e.g. ['py', 'python3']"
    )
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='skills'
    )

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
        related_name='job_roles'
    )
    skills = models.ManyToManyField(
        Skill,
        through='JobRoleSkill',
        related_name='job_roles',
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class JobRoleSkill(models.Model):
    class SkillImportance(models.TextChoices):
        REQUIRED = 'required', 'Required'
        PREFERRED = 'preferred', 'Preferred'
        BONUS = 'bonus', 'Bonus'

    job_role = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    importance = models.CharField(
        max_length=20,
        choices=SkillImportance.choices,
        default=SkillImportance.REQUIRED
    )

    class Meta:
        unique_together = ('job_role', 'skill')

    def __str__(self):
        return f"{self.skill.name} → {self.job_role.title} ({self.importance})"