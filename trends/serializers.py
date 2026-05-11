from rest_framework import serializers

from trends.models import JobTrend


class JobTrendSerializer(serializers.ModelSerializer):
    """
    Serialises a single JobTrend row for the dashboard.
    
    `formatted_growth` is included as a computed field — the frontend can
    use the raw `growth_7d` for sorting/charts and the formatted string
    for display.
    """
    formatted_growth = serializers.CharField(read_only = True)

    class Meta:
        model = JobTrend
        fields = [
            'name',
            'count',
            'percentage',
            'growth_7d',
            'formatted_growth',
            'skill', 
        ]

    