import datetime
import json

from jsrn.datetimeutil import to_ecma_date_string

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from apps.hello.models import Profile, Request
from apps.hello.forms import ProfileForm


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
        self.assertContains(response, reverse('requests'))

    def test_home_page_is_linked_to_edit_profile_page(self):  # noqa
        response = self.client.get(self.url)

        self.assertContains(response, reverse('edit_profile'))


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
        self.assertContains(response, reverse('home'))

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


class EditFormPageTest(TestCase):

    def setUp(self):
        self.url = reverse('edit_profile')

    def test_edit_form_view_displays_form(self):  # noqa
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/edit_form.html', 'hello/base.html']
        )
        self.assertContains(response, 'editForm')
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="surname"')
        self.assertContains(response, 'name="date_of_birth"')
        self.assertContains(response, 'name="bio"')
        self.assertContains(response, 'name="contact"')

    def test_edit_profile_page_is_linked_to_home_page(self):  # noqa
        response = self.client.get(self.url)

        # Can't use reverse here for '/'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/"')

    def test_edit_profile_view_renders_template_with_a_form(self):  # noqa
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ProfileForm)

    def test_edit_profile_view_populates_form_with_profile_data(self):  # noqa
        profile = Profile.objects.create(
            name='John',
            surname='Snow',
            bio='',
            date_of_birth=datetime.date.today(),
            contact='john.snow@mail.com'
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, profile.name)
        self.assertContains(response, profile.surname)
        self.assertContains(response, profile.contact)