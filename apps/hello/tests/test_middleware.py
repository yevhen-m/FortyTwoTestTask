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
            self.client.get(self.url, dict(name='John'))

        requests = Request.objects.all()

        self.assertEqual(requests.count(), 5)
        for r in requests:
            self.assertEqual(r.query, 'name=John')
            self.assertEqual(r.path, reverse('home'))
            self.assertEqual(r.method, 'GET')

    def test_middleware_does_not_save_ajax_requests(self):
        '''
        Test that middleware ignores ajax requests with query string
        `?store=false`.
        '''
        self.assertEqual(Request.objects.count(), 0)

        self.client.get(
            self.url,
            {'store': 'false'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(Request.objects.count(), 0)
