from django.shortcuts import render

from .models import Profile, Request


DISPLAY_TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def home(request):
    try:
        profile = Profile.objects.get(name='Yevhen')
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'hello/index.html', {'profile': profile})


def requests(request):
    requests = Request.objects.all()[:10]
    for r in requests:
        r.timestamp = r.timestamp.strftime(DISPLAY_TIMESTAMP_FORMAT)

    return render(request, 'hello/requests.html', {'requests': requests})
