from django.shortcuts import render,get_object_or_404
from .models import Domain, JobRole, Skill, SkillCategory

# Create your views here.
def job_roles_list(request):
    #Job roles list organized by domain
    domains = Domain.objects.prefetch_related('job_roles').all()
    return render(request, 'concepts/job_roles_list.html', {'domains': domains})

def job_role_detail(request, pk):
    # get the job role by pk
    job_role = get_object_or_404(JobRole, pk=pk)
    # get all skill categories that have skills for this role
    job_skills = Skill.objects.filter(job_role=job_role).select_related('category').order_by('category__order')
    # pass both to template
    return render(request, 'concepts/job_roles_detail.html', {'job_role': job_role, 'job_skills': job_skills})