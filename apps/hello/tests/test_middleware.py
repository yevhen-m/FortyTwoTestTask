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

    def test_middleware_saves_requests(self):  # noqa
        for _ in xrange(5):
            self.client.get(self.url)

        requests = Request.objects.all()

        self.assertEqual(requests.count(), 5)
