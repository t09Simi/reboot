from django.db.models import Max
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trends.models import JobTrend
from trends.serializers import JobTrendSerializer


class LatestTrendsView(APIView):
    """
    GET /api/trends/latest/

    Returns the most recent trend snapshot, grouped by trend type.
    Authenticated users only.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest_date = JobTrend.objects.aggregate(latest=Max('snapshot_date'))['latest']

        if latest_date is None:
            return Response({
                'snapshot_date': None,
                'sample_size': 0,
                'trends': {'skills': [], 'roles': [], 'companies': []},
            })

        rows = list(
            JobTrend.objects.filter(snapshot_date=latest_date)
                            .select_related('skill')
                            .order_by('-percentage')
        )

        sample_size = rows[0].sample_size if rows else 0

        type_to_key = {
            JobTrend.TrendType.SKILL: 'skills',
            JobTrend.TrendType.ROLE: 'roles',
            JobTrend.TrendType.COMPANY: 'companies',
        }
        grouped = {'skills': [], 'roles': [], 'companies': []}

        for row in rows:
            key = type_to_key.get(row.trend_type)
            if key:
                grouped[key].append(JobTrendSerializer(row).data)

        return Response({
            'snapshot_date': latest_date,
            'sample_size': sample_size,
            'trends': grouped,
        })