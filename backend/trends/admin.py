from django.contrib import admin
from .models import RawJobListing, JobTrend


@admin.register(RawJobListing)
class RawJobListingAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'employer_name', 'job_city', 'job_posted_at', 'fetched_at')
    list_filter = ('job_country', 'fetched_at')
    search_fields = ('job_title', 'employer_name', 'job_description')
    date_hierarchy = 'fetched_at'
    readonly_fields = ('fetched_at',)


@admin.register(JobTrend)
class JobTrendAdmin(admin.ModelAdmin):
    list_display = ('snapshot_date', 'trend_type', 'name', 'count', 'percentage', 'formatted_growth')
    list_filter = ('snapshot_date', 'trend_type')
    search_fields = ('name',)
    date_hierarchy = 'snapshot_date'