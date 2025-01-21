from django.db import models

from polygons.models import PolygonModel


class IntersectionModel(models.Model):
    class Meta:
        db_table = 'intersections'

    polygon_id = models.ForeignKey(PolygonModel, on_delete=models.CASCADE, related_name='intersections')
    intersected_id = models.ForeignKey(PolygonModel, on_delete=models.CASCADE, related_name='intersected_by')

    objects = models.Manager()  # или PyCharm Professional
