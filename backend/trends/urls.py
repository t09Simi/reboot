from django.urls import path

from trends.views import LatestTrendsView


app_name = 'trends'

urlpatterns = [
    path('latest/', LatestTrendsView.as_view(), name='latest'),
]