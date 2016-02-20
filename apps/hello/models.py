from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    bio = models.TextField()
    contact = models.EmailField()


class Request(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=300)
    query = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
