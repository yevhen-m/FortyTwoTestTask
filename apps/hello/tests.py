from django.test import TestCase
from django.test.utils import override_settings

from .models import Profile, Request
from .views import DISPLAY_TIMESTAMP_FORMAT


class HomePageTest(TestCase):
    fixtures = ['myfixture.json']

    def test_home_page(self):
        '''
        Test home page view.
        '''
        response = self.client.get('/')

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


class RequestsTest(TestCase):

    def test_requests_page(self):  # noqa
        response = self.client.get('/requests/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/requests.html', 'hello/base.html']
        )
        self.assertContains(response, 'GET')

        # Assert requests page is linked to index page
        self.assertContains(response, 'href="/"')

    def setUp(self):
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

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_shows_data_from_db(self):  # noqa
        r = Request.objects.first()
        r_display = '{} {} {} {}'.format(
            r.method,
            r.path,
            r.query,
            r.timestamp.strftime(DISPLAY_TIMESTAMP_FORMAT)
        )

        response = self.client.get('/requests/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('requests', response.context)
        self.assertContains(response, 'GET', count=3)
        self.assertContains(response, '/requests/')
        self.assertContains(response, '?page=2')
        self.assertContains(response, r_display)


class RequestsMiddlewareTest(TestCase):

    def test_middleware_is_registered_in_settings_module(self):
        from fortytwo_test_task.settings import MIDDLEWARE_CLASSES
        self.assertIn('apps.hello.middleware.RequestsMiddleware',
                      MIDDLEWARE_CLASSES)

    def test_middleware_saves_requests(self):  # noqa
        for _ in xrange(5):
            self.client.get('/')

        requests = Request.objects.all()

        self.assertEqual(requests.count(), 5)


class RequestTest(TestCase):

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_are_ordered_by_timestamp(self):
        kwargs = dict(method='GET',
                      path='/',
                      query='')
        for _ in xrange(3):
            Request.objects.create(**kwargs)

        r1, r2, r3 = Request.objects.all()

        self.assertGreater(r1.timestamp, r2.timestamp)
        self.assertGreater(r2.timestamp, r3.timestamp)
