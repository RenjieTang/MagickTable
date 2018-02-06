from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('v4/<id>/<z>/<x>/<y>', views.tile_request, name='tilerequest'),
]
