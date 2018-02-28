from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('v4/<id>/<z>/<x>/<y>', views.tile_request, name='tilerequest'),
    path('list', views.list, name='list'),
]
# + include('mapui.urls', namespace="mapui", app_name='mapui')
