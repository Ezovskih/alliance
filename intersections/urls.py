from django.urls import path

from intersections.views import check_intersections


urlpatterns = [
    path('check/', check_intersections, name='check_intersections'),
]
