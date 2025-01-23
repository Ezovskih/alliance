from django.contrib.admin import site as admin_site
from django.shortcuts import redirect
from django.urls import path, include

from app.views import account_login, account_logout


urlpatterns = [
    path('', lambda request: redirect('polygons/', permanent=True)),
    path('login/', account_login, name='account_login'),
    path('logout/', account_logout, name='account_logout'),
    path('admin/', admin_site.urls),
    path('polygons/', include('polygons.urls')),
    path('intersections/', include('intersections.urls')),
]
