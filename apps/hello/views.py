import json

from django.http import HttpResponse
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
    r_list = Request.objects.all()[:10]

    if request.is_ajax():
        page_request_id = int(request.GET['id'])
        new_requests = r_list[0].id - page_request_id

        for r in r_list:
            r.timestamp = r.timestamp.strftime(DISPLAY_TIMESTAMP_FORMAT)

        requests = {r.id: dict(method=r.method,
                               path=r.path,
                               query=r.query,
                               timestamp=r.timestamp)
                    for r in r_list}
        return HttpResponse(
            json.dumps({
                'new_requests': new_requests,
                'requests': requests
            }),
            content_type='application/json'
        )

    else:
        for r in r_list:
            r.timestamp = r.timestamp.strftime(DISPLAY_TIMESTAMP_FORMAT)

        return render(request, 'hello/requests.html', {'requests': r_list})
