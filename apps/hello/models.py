from PIL import Image

from django.db import models

PROFILE_PHOTO_SIZE = (200, 200)


class Profile(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    bio = models.TextField()
    email = models.EmailField()
    skype = models.CharField(max_length=30)
    jabber = models.EmailField()
    other_contacts = models.TextField()
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
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ('-timestamp',)


class DBAction(models.Model):
    model = models.CharField(max_length=30)
    action = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)
