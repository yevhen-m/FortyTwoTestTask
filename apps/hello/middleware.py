from .models import Request


class RequestsMiddleware(object):
    '''
    Stores all requests to the database.
    '''

    def process_request(self, request):
        Request.objects.create(
            method=request.method,
            path=request.path,
            query=request.META.get('query_string', '')
        )
