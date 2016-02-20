from django.test import TestCase

from .models import Profile, Request


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

    def test_requests_shows_data_from_db(self):
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
        r = Request.objects.create(
            method='GET',
            path='/',
            query='?page=2'
        )
        r_display = '{} {} {} {}'.format(
            r.method,
            r.path,
            r.query,
            r.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
        )

        response = self.client.get('/requests/')

        self.assertIn('requests', response.context)
        self.assertEqual(len(response.context['requests']), 3)
        self.assertContains(response, 'GET', count=3)
        self.assertContains(response, '/', count=2)
        self.assertContains(response, '/requests/')
        self.assertContaints(response, '?page=2')
        self.assertContains(response, r_display)
