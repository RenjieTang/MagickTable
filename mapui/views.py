from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the map ui index.")


def leaflet(request):
    file_name = request.GET.get("file")
    context = {'file': file_name}
    return render(request, 'leaflet_example.html', context)
