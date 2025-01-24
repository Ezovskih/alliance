from app.celery import application as celery

from polygons.models import PolygonModel
from intersections.models import IntersectionModel


@celery.task(max_retries=3)
def check_intersections(polygon_id):
    polygon: PolygonModel = PolygonModel.objects.filter(id=polygon_id).first()  # или None
    if polygon is None:
        return False

    # Находим пересекающиеся полигоны
    intersected_polygons = PolygonModel.objects.filter(
        shape__intersects=polygon.shape  # __overlaps без полностью вложенных
    ).exclude(id=polygon.pk)

    if not intersected_polygons.exists():
        send_message(polygon.user, "Полигон \"" + polygon.name + "\" прошел проверку!")
        return False

    # Удаляем имеющиеся записи о пересечениях
    IntersectionModel.objects.filter(polygon_id=polygon.pk).delete()

    for intersected in intersected_polygons:
        # Создаем новую запись о пересечении полигонов
        IntersectionModel.objects.create(polygon_id=polygon.pk, intersected_id=intersected.pk)

    send_message(
        user=polygon.user,
        text="Полигон \"" + polygon.name + "\" пересекается с полигонами:\n"
            + ', '.join(f"\"{x.name}\"" for x in intersected_polygons),
        link=polygon.link
    )
    return True

def send_message(user, text, link=None):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    channel_layer = get_channel_layer()
    sync_group_send = async_to_sync(channel_layer.group_send)
    sync_group_send(
        group=f"user_{user.id}_queue",
        message={'type': 'send_message', 'text': text, 'link': link}
    )
