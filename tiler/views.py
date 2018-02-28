from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.urls import reverse
from PIL import Image
import math
from tiler.forms import DocumentForm
from tiler.models.Document import Document as DocModel
from convertoimg.mpl import convert
import mapui


def index(request):
    return HttpResponse("Index page of tiler")


# TODO get this after tiling
max_tiles = 347

# this is got from what leaflet sends as x & y
start_x = 4091
start_y = 2721

# number of images on the x axis after tiling
n_x = 6
n_y = 58


# this is the function that will return a tile based on x, y, z
# TODO try different image formats
# TODO mapbox uses 256 by 256 squares: so we need to pad our generated image to fit that
def tile_request(request, id, z, x, y):
    # x 4091
    # y 2721

    x = int(x) - start_x
    y = int(y) - start_y
    print("(" + str(x) + ", " + str(y) + ")")
    if x < 0 or y < 0:
        return empty_response()
    x = int(math.fabs(x))
    y = int(math.fabs(y))
    i = coordinate(x, y)
    # print("i is ", i)
    if int(i) > max_tiles or int(x) >= n_x or int(y) >= n_y:
        return empty_response()
    print("(" + str(x) + ", " + str(y) + ") = " + i)
    pat = "/home/pavan/MagickTable/convertoimg/tiles/databig_tile" + i + ".png"
    # print(pat)
    try:
        with open(pat, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response


# handle file uploads
def list(request):
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
