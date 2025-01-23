from django.db import models

from polygons.models import PolygonModel


class IntersectionModel(models.Model):
    class Meta:
        db_table = 'intersections'

    polygon = models.ForeignKey(PolygonModel, on_delete=models.CASCADE, related_name='intersections')
    intersected = models.ForeignKey(PolygonModel, on_delete=models.CASCADE, related_name='intersected_by')

    objects = models.Manager()  # или PyCharm Professional
