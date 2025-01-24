from django.urls import reverse
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.auth.models import User


class PolygonModel(models.Model):
    class Meta:
        db_table = 'polygons'

    name = models.CharField(verbose_name="Название", unique=True)
    shape = models.PolygonField(verbose_name="Координаты")
    flag = models.BooleanField(verbose_name="Антимеридиан?", default=False, editable=False)
    # TODO flag = models.GeneratedField(expression=???, output_field=models.BooleanField(), db_persist=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()  # или PyCharm Professional

    @property
    def link(self):
        return reverse('polygon_update', args=[self.pk])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        [[69.3493386397765, 174.19921875000003], [69.3493386397765, 204.96093750000003],
        [62.103882522897884, 205.48828125000003], [62.186013857194226, 173.67187500000003]]
        """
        # Устанавливаем пересечение с антимеридианом
        antimeridian = GEOSGeometry('LINESTRING(180 -90, 180 90)')
        self.flag = GEOSGeometry(self.shape).intersects(antimeridian)

        super().save(*args, **kwargs)
