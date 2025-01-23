from http import HTTPStatus

from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from app import settings

from polygons.models import PolygonModel
from intersections.models import IntersectionModel


@csrf_exempt
async def check_intersections(request):
    print('REQUEST:', type(request), request)
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
    if not isinstance(polygon_id, int):
        return HttpResponseBadRequest()  # 400

    polygon = PolygonModel.objects.get(id=polygon_id)

    overlapped_polygons: QuerySet = PolygonModel.objects.exclude(id=polygon_id).filter(shape__overlaps=polygon.shape)
    if overlapped_polygons.exists():
        # Удаляем имеющиеся записи о пересечениях
        IntersectionModel.objects.filter(polygon_id=polygon_id).delete()

        for overlapped in overlapped_polygons:
            # Создаем новую запись о пересечении полигонов
            IntersectionModel.objects.create(polygon_id=polygon, intersected_id=overlapped)

        # Уведомляем пользователя
        _send_intersection_alert(polygon, overlapped_polygons)

        return HttpResponse(HTTPStatus.ACCEPTED)  # 202

    return HttpResponse(status=HTTPStatus.NO_CONTENT)  # 204

def _send_intersection_alert(polygon, overlapped_polygons):
    sync_group_send = async_to_sync(get_channel_layer().group_send)
    sync_group_send(
        group='public_alerts',  # TODO f"user_{user.id}",
        message={
            'type': 'send_polygon_alert',
            'polygon_id': polygon.pk,
            'message': "Полигон \"" + polygon.name + "\" пересекается с полигонами:\n" +
                ', '.join(f"\"{x.name}\"" for x in overlapped_polygons)
        }
    )

def _send_message(message):
    sync_group_send = async_to_sync(get_channel_layer().group_send)
    sync_group_send(group='public_alerts',
        message={'type': 'send_message', 'message': message})
