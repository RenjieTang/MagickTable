import math

import os
from PIL import Image
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

from convertoimg.mpl import convert
from tiler.forms import DocumentForm
from tiler.models.Document import Document as DocModel


def index(request):
    return HttpResponse("Index page of tiler")


# TODO get this after tiling
max_tiles = 15

# this is got from what leaflet sends as x & y
start_x = 4091
start_y = 2722

# number of images on the x axis after tiling
n_x = 5
n_y = 3


# this is the function that will return a tile based on x, y, z
# TODO try different image formats
# TODO mapbox uses 256 by 256 squares: so we need to pad our generated image to fit that
def tile_request(request, id, z, x, y):
    file_name = request.GET.get("file")
    # x 4091
    # y 2721

    # print("x = ", x, " y = ", y)
    x = int(x) - start_x
    y = int(y) - start_y
    # print("(" + str(x) + ", " + str(y) + ")")
    if x < 0 or y < 0:
        return empty_response()
    x = int(math.fabs(x))
    y = int(math.fabs(y))
    i = coordinate(x, y)
    # print("i is ", i)
    if int(i) > max_tiles or int(x) >= n_x or int(y) >= n_y:
        return empty_response()
    # print("(" + str(x) + ", " + str(y) + ") = " + i)
    # path = os.path.join(settings.MEDIA_ROOT, file_name + '.png')
    path = os.path.join(settings.MEDIA_ROOT, 'tiles', 'documents', file_name + i + ".png");
    pat = "/home/pavan/MagickTable/convertoimg/tiles/databig_tile" + i + ".png"
    # print(pat)
    print(path)
    try:
        with open(path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response


# handle file uploads
def list_files(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = DocModel(docfile=request.FILES['docfile'])
            newdoc.save()
            convert(newdoc.docfile.name)
            # TODO this will not work with files of same name
            return redirect('/map/leaflet?file=' + request.FILES['docfile'].name)

    else:
        form = DocumentForm()

    documents = DocModel.objects.all()
    return render(request, 'list.html',
                  {'documents': documents, 'form': form}
                  )


def empty_response():
    red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    response = HttpResponse(content_type="image/png")
    red.save(response, "png")
    return response


def coordinate(x, y):
    # i + nx * (j + ny * k)
    tile_number = x + n_x * y
    return str(tile_number).zfill(3).replace("-", "0")
