import json

from jsrn.datetimeutil import to_ecma_date_string

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers

from .models import Profile, Request


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
        requests = serializers.serialize('json', r_list)
        # Django serializes datetime objects according to ecma 262
        return HttpResponse(
            json.dumps({
                'new_requests': new_requests,
                'requests': requests
            }),
            content_type='application/json'
        )
    else:
        for r in r_list:
            # Need to display data in this format
            r.timestamp = to_ecma_date_string(r.timestamp)
        return render(request, 'hello/requests.html', {'requests': r_list})
