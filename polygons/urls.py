from django.urls import path

from polygons.views import polygon_list, polygon_create, polygon_update, polygon_delete


# app_name = 'polygons'  # используется как префикс к ссылке

urlpatterns = [
    path('', polygon_list, name='polygon_list'),
    path('create/', polygon_create, name='polygon_create'),
    path('update/<int:pk>/', polygon_update, name='polygon_update'),
    path('delete/<int:pk>/', polygon_delete, name='polygon_delete'),
]
