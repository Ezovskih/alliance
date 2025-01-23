from django.core.serializers import serialize
from django.http import Http404, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from polygons.models import PolygonModel
from polygons.forms import PolygonForm


def _check_intersections(polygon_id):
    from requests import post
    from app.settings import INTERSECTIONS_API_URL, INTERSECTIONS_API_KEY

    print('POLYGON ID:', polygon_id, type(polygon_id))
    data = {'polygon_id': polygon_id}
    headers = {'Authorization': f"Bearer {INTERSECTIONS_API_KEY}"}
    try:
        post(INTERSECTIONS_API_URL, json=data, headers=headers)
    except Exception as error:
        print(error)

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
            polygon.save()

            _check_intersections(polygon.pk)
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
    if polygon.user != request.user:
        return HttpResponseForbidden()  # 403
    elif not request.user.is_superuser:  # исключение
        pass

    if request.method == "POST":
        form = PolygonForm(request.POST, instance=polygon)
        if form.is_valid():
            polygon = form.save()

            _check_intersections(polygon.pk)
            return redirect('polygon_list')
    else:
        form = PolygonForm(instance=polygon)

    return render(request, 'polygon_form.html', {'form': form, 'shape': polygon.shape})

def polygon_delete(request, pk):
    # Аутентифицируем пользователя
    if not request.user.is_authenticated:
        return redirect('account_login')

    polygon: PolygonModel = get_object_or_404(PolygonModel, pk=pk)

    # Авторизуем пользователя
    if polygon.user != request.user:
        return HttpResponseForbidden()  # 403
    elif request.user.is_superuser:  # исключение
        pass

    if request.method == "POST":
        polygon.delete()

        return redirect('polygon_list')

    return render(request, 'confirm_delete.html', {'polygon': polygon})
