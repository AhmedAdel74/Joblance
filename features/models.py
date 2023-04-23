from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from project import settings
from project.settings import MEDIA_ROOT
from PIL import Image
from django.db.models.signals import post_save
from django.utils.text import slugify


def image_upload(instance, filename):
    imagename, extension = filename.split(".")
    return "craftsmen/%s/%s" % (instance.id, extension)


class Craftsmen(models.Model):

    image = models.ImageField(default='user.png', upload_to=image_upload)
    name = models.CharField(max_length=30, default='none')
    slug = models.SlugField(null=True, blank=True)
    phone_number = models.IntegerField(default='none')
    profession = models.CharField(max_length=30, default='none')
    address = models.CharField(max_length=50, default='none')
    working_hours = models.CharField(max_length=50, default='none')
    description = models.TextField(max_length=10000)

    def __str__(self):
        return str(self.name)
