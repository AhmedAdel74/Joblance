from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from project import settings
from project.settings import MEDIA_ROOT
from PIL import Image
from django.db.models.signals import post_save
from django.utils.text import slugify
from urllib.parse import urlparse
# محتاجة تعملى migrations و migrate
# Create your models here.


def image_upload(instance, filename):
    imagename, extension = filename.split(".")
    return "profile/%s/%s" % (instance.id, extension)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    # بتستدعى ال attribute دة
    ##
    image = models.ImageField(default='user.png', upload_to=image_upload)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    email = models.EmailField(max_length=30, default='none')
    phone_number = models.CharField(max_length=15, default='none')
    # age=models.CharField(max_length=15 ,default='none')
    city = models.CharField(max_length=30, default='none')
    gender = models.CharField(max_length=15, default='male')
    education = models.CharField(default='none', max_length=200)
    tecskill = models.CharField(default='none', max_length=200)
    softskill = models.CharField(default='none', max_length=200)
    language = models.CharField(default='none', max_length=200)
    experience = models.CharField(default='none', max_length=400)
    bio = models.TextField(default='none')
    dob = models.DateField(blank=True, null=True)
    cv = models.FileField(upload_to=user_directory_path,
                          max_length=40, default='none')
    file = models.FileField(upload_to=user_directory_path,
                            max_length=40, default='none')
    face=models.CharField(null=False,blank=False, max_length=200)
    

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.user)
    
    face_name = models.CharField(null=True, blank=True, max_length=200)

    def save(self, *args, **kwargs):
        if self.face:
            parsed_url = urlparse(self.face)
            path = parsed_url.path
            if path.startswith('/'):
                path = path[1:]
            if path.endswith('/'):
                path = path[:-1]
            name = path.split('/')[-1]
            self.face_name = name
        super().save(*args, **kwargs)

    # def save(self):
        # super().save()

        # img = Image.open(self.image.path)

        # if img.height > 300 or img.width >300:
        # output_size = (300,300)
        # img.thumbnail(output_size)
        # img.save(self.image.path)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
