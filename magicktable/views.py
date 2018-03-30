from django.shortcuts import render, redirect

from tiler.forms import DocumentForm
from tiler.models.Document import Document
from tiler.views import convert_html


def file_exists_in_db(file_name):
    docs = Document.objects.filter(file_name=file_name)
    if not docs:
        return False
    else:
        return True


def list_files(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid() and not file_exists_in_db(request.FILES['docfile'].name):
            newdoc = Document(file_name=request.FILES['docfile'].name, docfile=request.FILES['docfile'])
            newdoc.save()
            convert_html(newdoc, newdoc.file_name)
            # TODO this will not work with files of same name
            return redirect('/map/leaflet?file=' + request.FILES['docfile'].name)

    else:
        form = DocumentForm()

    documents = Document.objects.all()
    return render(request, 'list.html',
                  {'documents': documents, 'form': form}
                  )
