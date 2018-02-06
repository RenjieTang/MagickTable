from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the map ui index.")


def leaflet(request):
    context = {}
    return render(request, 'leaflet_example.html', context)
