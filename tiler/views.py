from django.http import HttpResponse
from PIL import Image
from django.conf import settings
import os


def index(request):
    return HttpResponse("Index page of tiler")


# this is the function that will return a tile based on x, y, z
# TODO try different image formats
def tile_request(request, id, z, x, y):
    # x 4093
    # y 2723

    x = int(x) - 4093
    y = int(y) - 2723

    i = coordinate(x, y)
    print("i is ", int(i))
    if int(i) > 43:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response
    pat = "tile" + i + ".png"
    try:
        with open(pat, "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "png")
        return response


def coordinate(x, y):
    # i + nx * (j + ny * k)
    tile_number = x + 4 * y
    return str(tile_number).zfill(3).replace("-", "0")
