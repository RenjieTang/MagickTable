from django.http import HttpResponse
from PIL import Image
from django.conf import settings
import os


def index(request):
    return HttpResponse("Index page of tiler")


# this is the function that will return a tile based on x, y, z
# TODO try different image formats
def tile_request(request, id, z, x, y):
    try:
        with open("/home/pavan/MagickTable/tiler/static/plain.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/jpeg")
        red.save(response, "JPEG")
        return response
