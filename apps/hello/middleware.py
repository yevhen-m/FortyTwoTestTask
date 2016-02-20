from .models import Request


class RequestsMiddleware(object):
    '''
    Stores all requests to the database.
    '''

    def process_request(self, request):  # noqa
        if request.is_ajax() and request.GET.get('store') == 'false':
            return
        else:
            Request.objects.create(
                method=request.method,
                path=request.path,
                query=request.META.get('query_string', '')
            )
