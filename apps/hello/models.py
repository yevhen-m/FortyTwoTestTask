from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    bio = models.TextField()
    contact = models.EmailField()
    photo = models.ImageField(upload_to='images', blank=True, null=True)


class Request(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=300)
    query = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
