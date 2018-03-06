from django.db import models


class Document(models.Model):
    # TODO change this to username?
    docfile = models.FileField(upload_to='documents/')
