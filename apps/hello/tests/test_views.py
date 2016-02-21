import json

from jsrn.datetimeutil import to_ecma_date_string

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from apps.hello.models import Profile, Request


class HomePageTest(TestCase):
    fixtures = ['myfixture.json']

    def setUp(self):
        self.url = reverse('home')

    def test_home_view(self):  # noqa
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/index.html', 'hello/base.html']
        )
        self.assertIn('profile', response.context)

        profile = Profile.objects.get(name='Yevhen')
        c = response.context

        self.assertIsInstance(c['profile'], Profile)
        self.assertEqual(c['profile'].name, profile.name)
        self.assertEqual(c['profile'].surname, profile.surname)

        self.assertContains(response, 'Yevhen')
        self.assertContains(response, 'Malov')
        self.assertContains(response, 'My bio')
        self.assertContains(response, 'yvhn.yvhn@gmail.com')

        # Assert index page is linked to requests page
        self.assertContains(response, 'href="/requests/"')


class RequestsPageTest(TestCase):

    def setUp(self):
        self.url = reverse('requests')

        Request.objects.create(
            method='GET',
            path='/',
            query=''
        )
        Request.objects.create(
            method='GET',
            path='/requests/',
            query=''
        )
        Request.objects.create(
            method='GET',
            path='/',
            query='?page=2'
        )

    def test_requests_view(self):  # noqa
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/requests.html', 'hello/base.html']
        )
        self.assertContains(response, 'GET')

        # Assert requests page is linked to index page
        self.assertContains(response, 'href="/"')

    @override_settings(MIDDLEWARE_CLASSES=())  # noqa
    def test_requests_view_shows_data_from_db(self):  # noqa
        r = Request.objects.first()
        r_display = '{} {} {} {}'.format(
            r.method,
            r.path,
            r.query,
            to_ecma_date_string(r.timestamp)
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('requests', response.context)
        self.assertContains(response, 'GET', count=3)
        self.assertContains(response, '/requests/')
        self.assertContains(response, '?page=2')
        self.assertContains(response, r_display)

    def test_requests_view_limits_requests_on_the_page(self):  # noqa
        for _ in xrange(15):
            response = self.client.get(self.url)

        self.assertEqual(len(response.context['requests']), 10)

    @override_settings(MIDDLEWARE_CLASSES=())  # noqa
    def test_requests_view_handles_ajax_requests(self):  # noqa
        response = self.client.get(
            self.url,
            {'id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        try:
            data = json.loads(response.content)
        except ValueError:
            self.fail('requests view does not return json response content')

        self.assertIn('new_requests', data)
        self.assertEqual(data['new_requests'], 2)
        self.assertIn('requests', data)
        # data['requests'] is a serialized query set, so I need to turn it into
        # a list
        requests = json.loads(data['requests'])
        self.assertEqual(len(requests), 3)
