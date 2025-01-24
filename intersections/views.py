from http import HTTPStatus

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from app import settings
from app.consumers import NotificationConsumer

from polygons.models import PolygonModel
from intersections.models import IntersectionModel


@csrf_exempt
async def check_intersections(request):
    # Проверяем используемый метод
    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods='POST')  # 405

    # Проверяем API-ключ в заголовке
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != f"Bearer {settings.INTERSECTIONS_API_KEY}":
        http_response_unauthorized = HttpResponse(status=HTTPStatus.UNAUTHORIZED)  # 401
        http_response_unauthorized['WWW-Authenticate'] = 'Bearer realm="intersections"'
        return http_response_unauthorized

    # Проверяем параметры запроса
    polygon_id = request.POST.get('polygon_id')
    if not isinstance(polygon_id, int):  # TODO list?
        return HttpResponseBadRequest()  # 400

    polygon = PolygonModel.objects.get(id=polygon_id)

    x_polygons = PolygonModel.objects.filter(shape__intersets=polygon.shape).exclude(id=polygon_id)
    if x_polygons.exists():
        # Удаляем имеющиеся записи о пересечениях
        IntersectionModel.objects.filter(polygon_id=polygon_id).delete()

        for x_polygon in x_polygons:
            # Создаем новую запись о пересечении полигонов
            IntersectionModel.objects.create(polygon_id=polygon, intersected_id=x_polygon)

        # Уведомляем пользователя
        _send_message_with_url(polygon, x_polygons)

        return HttpResponse(HTTPStatus.ACCEPTED)  # 202

    return HttpResponse(status=HTTPStatus.NO_CONTENT)  # 204

def _send_message_with_url(polygon, x_polygons):
    sync_group_send = async_to_sync(get_channel_layer().group_send)
    sync_group_send(
        group=NotificationConsumer.group_name,
        message={
            'type': 'send_message_with_url',
            'message': "Полигон \"" + polygon.name + "\" пересекается с полигонами:\n" +
                ', '.join(f"\"{x.name}\"" for x in x_polygons),
            'url': reverse('polygon_update', args=(polygon.pk,)),
        }
    )

def _send_message(message):
    sync_group_send = async_to_sync(get_channel_layer().group_send)
    sync_group_send(group=NotificationConsumer.group_name,
        message={'type': 'send_message', 'message': message})
