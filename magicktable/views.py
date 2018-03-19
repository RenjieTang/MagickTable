from django.shortcuts import render, redirect

from tiler.forms import DocumentForm
from tiler.models.Document import Document as DocModel
from tiler.views import convert_html


def list_files(request):
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
