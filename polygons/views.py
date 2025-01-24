from django.core.serializers import serialize
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound

from app.tasks import check_intersections

from polygons.models import PolygonModel
from polygons.forms import PolygonForm
from intersections.models import IntersectionModel


def polygon_list(request):
    # Аутентифицируем пользователя
    if not request.user.is_authenticated:
        return redirect('account_login')

    # Авторизуем пользователя
    if request.user.is_superuser:
        polygons = PolygonModel.objects.all()
    else:
        polygons = PolygonModel.objects.filter(user=request.user)

    # Используем GeoJSON для передачи гео-данных клиенту
    geo_json = serialize('geojson', polygons, geometry_field='shape')  # pk вместо id
    return render(request, 'polygon_list.html', {'geo_json': geo_json, 'polygons': polygons})


def polygon_create(request):
    # Аутентифицируем пользователя
    if not request.user.is_authenticated:
        return redirect('account_login')

    if request.method == "POST":
        form = PolygonForm(request.POST)
        if form.is_valid():
            polygon = form.save(commit=False)
            polygon.user = request.user
            polygon.save()  # commit

            check_intersections.delay_on_commit(polygon.pk)  # ~ transaction.on_commit
            return redirect('polygon_list')
    else:
        form = PolygonForm()

    return render(request, 'polygon_form.html', {'form': form})


def polygon_update(request, pk):
    # Аутентифицируем пользователя
    if not request.user.is_authenticated:
        return redirect('account_login')

    try:
        polygon: PolygonModel = get_object_or_404(PolygonModel, pk=pk)
    except Http404:
        return HttpResponseNotFound()  # 404

    # Авторизуем пользователя
    if request.user.is_superuser:
        pass
    elif polygon.user != request.user:
        return HttpResponseForbidden()  # 403

    if request.method == "POST":
        form = PolygonForm(request.POST, instance=polygon)
        if form.is_valid():
            polygon = form.save()

            check_intersections.delay_on_commit(polygon.pk)  # ~ transaction.on_commit
            return redirect('polygon_list')
    else:
        form = PolygonForm(instance=polygon)

    # Находим пересекающиеся полигоны
    intersections = IntersectionModel.objects.filter(polygon_id=polygon.pk).values_list('intersected_id', flat=True)
    intersected_polygons = PolygonModel.objects.filter(pk__in=intersections)
    # Используем GeoJSON для передачи координат пересекающих полигонов
    geo_json = serialize('geojson', intersected_polygons, geometry_field='shape')  # pk вместо id

    return render(request, 'polygon_form.html', {'form': form, 'intersections': geo_json})


def polygon_delete(request, pk):
    # Аутентифицируем пользователя
    if not request.user.is_authenticated:
        return redirect('account_login')

    try:
        polygon: PolygonModel = get_object_or_404(PolygonModel, pk=pk)
    except Http404:
        return HttpResponseNotFound()  # 404

    # Авторизуем пользователя
    if request.user.is_superuser:
        pass
    elif polygon.user != request.user:
        return HttpResponseForbidden()  # 403

    if request.method == "POST":
        polygon.delete()

        return redirect('polygon_list')

    return render(request, 'confirm_delete.html', {'polygon': polygon})
