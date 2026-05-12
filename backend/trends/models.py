from django.db import models


class RawJobListing(models.Model):
    """
    Raw job listing as fetched from the upstream source (JSearch).
    Minimally processed. Kept around so we can re-run aggregation
    if our extraction logic changes.
    """
    # Deduplication
    job_id = models.CharField(max_length=200, unique=True)
    
    # Aggregation fields
    job_title = models.CharField(max_length=300)
    employer_name = models.CharField(max_length=300, blank=True)
    job_city = models.CharField(max_length=200, blank=True)
    job_country = models.CharField(max_length=10, blank=True)
    job_description = models.TextField()                        
    job_posted_at = models.DateTimeField(null=True, blank=True)
    job_min_salary = models.IntegerField(null=True, blank=True)
    job_max_salary = models.IntegerField(null=True, blank=True)
    
    # Bookkeeping
    fetched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fetched_at']
        indexes = [
            models.Index(fields=['job_posted_at']),                # for time-based queries
            models.Index(fields=['fetched_at']),
        ]
    
    def __str__(self):
        return f"{self.job_title} @ {self.employer_name}"
    

class JobTrend(models.Model):
    """
    Aggregated trend snapshot computed from RawJobListing data.
    
    One row per (trend_type, name, snapshot_date). Each aggregation run
    creates a new batch of rows — historical snapshots are preserved
    so we can compute growth and show long-term trend charts.
    """
    
    class TrendType(models.TextChoices):
        SKILL = 'skill', 'Skill'
        ROLE = 'role', 'Job Role'
        COMPANY = 'company', 'Company'
    
    trend_type = models.CharField(
        max_length=20,
        choices=TrendType.choices,
    )
    name = models.CharField(max_length=200)                       # display name, always present
    skill = models.ForeignKey(                                    # only set when trend_type == 'skill'
        'concepts.Skill',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='trends'
    )
    
    # Aggregation results
    count = models.PositiveIntegerField()                         # raw count of listings
    percentage = models.FloatField()                              # % of listings in the snapshot window
    growth_7d = models.FloatField(null=True, blank=True)          # % change vs previous snapshot; null if no prior
    
    # Snapshot metadata
    snapshot_date = models.DateField()                            # the date the aggregation ran
    sample_size = models.PositiveIntegerField()                   # total listings in the snapshot window (for context)
    
    class Meta:
        ordering = ['-snapshot_date', 'trend_type', '-percentage']
        constraints = [
            models.UniqueConstraint(
                fields=['trend_type', 'name', 'snapshot_date'],
                name='unique_trend_per_snapshot'
            )
        ]
        indexes = [
            models.Index(fields=['snapshot_date', 'trend_type']),  # dashboard's main query
        ]
    
    def __str__(self):
        return f"[{self.snapshot_date}] {self.get_trend_type_display()}: {self.name} ({self.percentage:.1f}%)"
    
    @property
    def formatted_growth(self):
        """For display: '↑ 12.5%' / '↓ 3.2%' / '—'"""
        if self.growth_7d is None:
            return '—'
        arrow = '↑' if self.growth_7d > 0 else ('↓' if self.growth_7d < 0 else '→')
        return f"{arrow} {abs(self.growth_7d):.1f}%"