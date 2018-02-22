from django.http import HttpResponse
from PIL import Image
import math


def index(request):
    return HttpResponse("Index page of tiler")


# TODO get this after tiling
max_tiles = 14

# this is got from what leaflet sends as x & y
start_x = 4091
start_y = 2721

# number of images on the x axis after tiling
n_x = 5
n_y = 3


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
    if int(i) > 14 or int(x) >= n_x or int(y) >= n_y:
        return empty_response()
    print("(" + str(x) + ", " + str(y) + ") = " + i)
    pat = "/home/pavan/MagickTable/convertoimg/tiles/sample_tile" + i + ".png"
    # print(pat)
    try:
        with open(pat, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response


def empty_response():
    red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
    response = HttpResponse(content_type="image/png")
    red.save(response, "png")
    return response


def coordinate(x, y):
    # i + nx * (j + ny * k)
    tile_number = x + n_x * y
    return str(tile_number).zfill(3).replace("-", "0")
