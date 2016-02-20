from django.shortcuts import render

from .models import Profile


def home(request):
    profile = Profile.objects.get(name='Yevhen')
    return render(request, 'hello/index.html', {'profile': profile})


def requests(request):
    return render(request, 'hello/requests.html')
