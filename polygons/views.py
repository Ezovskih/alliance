from django.core.serializers import serialize
from django.shortcuts import render, redirect, get_object_or_404

from .models import PolygonModel
from .forms import PolygonForm


def polygon_list(request):
    polygons = PolygonModel.objects.all()

    # Используем GeoJSON для передачи гео-данных в JavaScript
    geo_json = serialize('geojson', polygons, geometry_field='shape')  # pk вместо id
    return render(request, 'polygon_list.html', {'geo_json': geo_json, 'polygons': polygons})


def polygon_create(request):
    if request.method == "POST":
        form = PolygonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polygon_list')
    else:
        form = PolygonForm()

    return render(request, 'polygon_form.html', {'form': form})


def polygon_update(request, pk):
    polygon: PolygonModel = get_object_or_404(PolygonModel, pk=pk)

    if request.method == "POST":
        form = PolygonForm(request.POST, instance=polygon)
        if form.is_valid():
            form.save()
            return redirect('polygon_list')
    else:
        form = PolygonForm(instance=polygon)

    return render(request, 'polygon_form.html', {'form': form, 'shape': polygon.shape})


def polygon_delete(request, pk):
    polygon: PolygonModel = get_object_or_404(PolygonModel, pk=pk)

    if request.method == "POST":
        polygon.delete()
        return redirect('polygon_list')

    return render(request, 'confirm_delete.html', {'polygon': polygon})
