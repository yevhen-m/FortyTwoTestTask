from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings

from apps.hello.models import Request


class RequestsMiddlewareTest(TestCase):

    def setUp(self):
        self.url = reverse('home')

    def test_middleware_is_registered_in_settings_module(self):
        '''
        Test that my middleware class is registered in settings.py
        '''
        self.assertIn(
            'apps.hello.middleware.RequestsMiddleware',
            settings.MIDDLEWARE_CLASSES
        )

    def test_middleware_saves_requests(self):
        '''
        Test my middleware stores requests to db.
        '''
        for _ in xrange(5):
            self.client.get(self.url)

        requests = Request.objects.all()

        self.assertEqual(requests.count(), 5)

    def test_middleware_does_not_save_ajax_requests(self):
        '''
        Test that middleware ignores ajax requests with query string
        `?store=false`.
        '''
        # Request model is ordered my timestamp descending
        for _ in xrange(12):
            Request.objects.create(
                method='GET',
                path='/',
                query=''
            )

        newest_request_id_before_ajax_request = Request.objects.first().id

        self.client.get(
            self.url,
            {'store': 'false'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        newest_request_id_after_ajax_request = Request.objects.first().id

        self.assertEqual(
            newest_request_id_before_ajax_request,
            newest_request_id_after_ajax_request
        )
