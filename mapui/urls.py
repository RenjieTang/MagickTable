from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='mapui_index'),
    path('leaflet', views.leaflet, name='leaflet'),
]
