from PIL import Image

from django.db import models

PROFILE_PHOTO_SIZE = (200, 200)


class Profile(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    bio = models.TextField()
    contact = models.EmailField()
    photo = models.ImageField(upload_to='images', blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        try:
            image_path = self.photo.path
        except ValueError:
            return

        try:
            image = Image.open(image_path)
        except IOError:
            return
        image.thumbnail(PROFILE_PHOTO_SIZE, Image.ANTIALIAS)
        image.save(image_path)


class Request(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=300)
    query = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
