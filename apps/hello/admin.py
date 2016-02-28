from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import *  # noqa


admin.site.register(Profile)
admin.site.register(Request)
admin.site.register(DBAction)
admin.site.register(LogEntry)
