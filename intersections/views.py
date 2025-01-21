from polygons.models import PolygonModel
from intersections.models import IntersectionModel


def check_intersections(polygon: PolygonModel):
    intersections = PolygonModel.objects.exclude(id=polygon.pk).filter(shape__overlaps=polygon.shape)
    if intersections.exists():
        for intersected in intersections:
            IntersectionModel.objects.get_or_create(polygon_id=polygon, intersected_id=intersected)

        send_intersection_alert(polygon, intersections)


def send_intersection_alert(polygon: PolygonModel, intersections):
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    sync_group_send = async_to_sync(get_channel_layer().group_send)
    sync_group_send(
        group='public_alerts',
        message={
            'type': 'send_polygon_alert',
            'polygon_id': polygon.pk,
            'alert_text': "Полигон \"" + polygon.name + "\" пересекается с полигонами:\n" +
                ', '.join(f"\"{x.name}\"" for x in intersections)
        }
    )
