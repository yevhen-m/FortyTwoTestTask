import json

from jsrn.datetimeutil import to_ecma_date_string

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import Profile, Request
from .forms import ProfileForm


def home(request):
    try:
        profile = Profile.objects.filter(name='Yevhen', surname='Malov')[0]
    except IndexError:
        profile = None

    return render(request, 'hello/index.html', {'profile': profile})


def requests(request):
    priority = request.GET.get('priority')
    if priority is not None:
        try:
            priority = int(priority)
        except (ValueError, TypeError):
            priority = 1

        order_by = '{}priority'.format('-' if priority else '')
        r_list = Request.objects.all().order_by(order_by, '-timestamp')[:10]
    else:
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
        return render(request, 'hello/requests.html', {'requests': r_list,
                                                       'priority': priority})


@login_required
def edit_profile(request):
    profile = Profile.objects.first()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponse('')
        else:
            return HttpResponseBadRequest(
                json.dumps(form.errors),
                content_type='application/json'
            )
    else:
        form = ProfileForm(instance=profile)
        return render(request, 'hello/edit_form.html', {'form': form})
