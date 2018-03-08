import math
import os

import imgkit
import pandas as pd
from PIL import Image
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

from convertoimg.mpl import slice_image
from tiler.forms import DocumentForm
from tiler.models.Document import Document as DocModel


def index(request):
    return HttpResponse("Index page of tiler")


tile_count_on_x = 14
tile_count_on_y = 99
total_tile_count = 900

rows_per_image = 500

# todo: this is got from what leaflet sends as x & y
start_x = 4091
start_y = 2722


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
    if int(i) > total_tile_count or int(x) >= tile_count_on_x or int(y) >= tile_count_on_y:
        return empty_response()
    print("tile for (" + str(x) + ", " + str(y) + ") = " + i)
    # path = os.path.join(settings.MEDIA_ROOT, file_name + '.png')
    path = os.path.join(settings.MEDIA_ROOT, 'tiles', 'documents', file_name + i + ".jpg");
    # print("tile path = {}".format(path))
    # pat = "/home/pavan/MagickTable/convertoimg/tiles/databig_tile" + i + ".png"
    # print(pat)
    # print(path)
    try:
        with open(path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpg")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpg")
        red.save(response, "png")
        return response


# handle file uploads
def list_files(request):
    global tile_count_on_x
    global tile_count_on_y
    global total_tile_count
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = DocModel(docfile=request.FILES['docfile'])
            newdoc.save()
            convert_html(newdoc.docfile.name)
            # TODO this will not work with files of same name
            # print("final", tile_count_on_x, tile_count_on_y, total_tile_count)
            return redirect('/map/leaflet?file=' + request.FILES['docfile'].name)

    else:
        form = DocumentForm()

    documents = DocModel.objects.all()
    return render(request, 'list.html',
                  {'documents': documents, 'form': form}
                  )


def convert_html(csv_name):
    csv = pd.read_csv(os.path.join(settings.MEDIA_ROOT, csv_name))
    num_lines = csv.shape[0]
    x = 0
    global tile_count_on_x
    global tile_count_on_y
    global total_tile_count
    tile_count_on_x = 0
    tile_count_on_y = 0
    total_tile_count = 0
    number_of_cols = 0
    number_of_rows = 0
    tile_count = 0
    while x < num_lines:
        df = csv[x:x + rows_per_image]
        html = df.to_html()
        # rendered = render_to_string('table.html', {'csv_path': os.path.join(settings.MEDIA_ROOT, csv_name)})
        imgkit.from_string(html, os.path.join(settings.MEDIA_ROOT, csv_name + str(x) + '.jpg'))
        number_of_cols, number_of_rows, tile_count = slice_image(csv_name, os.path.join(settings.MEDIA_ROOT,
                                                                                        csv_name + str(x) + '.jpg'),
                                                                 tile_count)
        tile_count_on_y += number_of_rows
        tile_count_on_x = number_of_cols
        # print("rows = {}\tx_n {}\t y_n {}\t tiles {}".format(x, tile_count_on_x, tile_count_on_y, tile_count))
        x += rows_per_image
    total_tile_count = tile_count
    # print("done converting")


def empty_response():
    red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    response = HttpResponse(content_type="image/png")
    red.save(response, "png")
    return response


def coordinate(x, y):
    # i + nx * (j + ny * k)
    tile_number = x + tile_count_on_x * y
    return str(tile_number).zfill(3).replace("-", "0")
