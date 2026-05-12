from django.contrib import admin
from .models import Domain, SkillCategory, Skill, JobRole, JobRoleSkill


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    ordering = ('order',)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order', 'name')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class JobRoleSkillInline(admin.TabularInline):
    model = JobRoleSkill
    extra = 1


@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'is_active')
    list_filter = ('domain', 'is_active')
    search_fields = ('title',)
    inlines = [JobRoleSkillInline]


@admin.register(JobRoleSkill)
class JobRoleSkillAdmin(admin.ModelAdmin):
    list_display = ('job_role', 'skill', 'importance')
    list_filter = ('importance',)