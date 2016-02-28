import datetime
import json

from jsrn.datetimeutil import to_ecma_date_string

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.contrib.auth.models import User

from apps.hello.models import Profile, Request
from apps.hello.forms import ProfileForm


class HomePageTest(TestCase):
    fixtures = ['myfixture.json']

    def setUp(self):
        self.url = reverse('home')

    def test_home_view(self):
        '''
        Test that home page view works, renders the right template with
        the right context and shows my profile data from db.
        '''
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

    def test_home_page_works_with_no_profiles_in_db(self):
        '''
        Test that my page works, when there are no profiles in the
        database.
        '''
        Profile.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_home_page_is_linked_to_edit_profile_page(self):
        '''
        Test for a link to edit_profile page on the home page.
        '''
        response = self.client.get(self.url)

        self.assertContains(response, reverse('edit_profile'))

    def test_home_page_is_linked_to_edit_page(self):
        '''
        Test for a link to login page on the home page.
        '''
        response = self.client.get(self.url)

        self.assertContains(response, reverse('login'))

    def test_admin_link_on_home_page(self):
        '''
        Test that there is a link to admin edit page on the home page.
        '''
        profile = Profile.objects.get(name='Yevhen')
        self.assertIsNotNone(profile)

        response = self.client.get(self.url)
        self.assertContains(response, 'Yevhen')
        self.assertContains(
            response,
            reverse('admin:hello_profile_change', args=(profile.pk,))
        )


class RequestsPageTest(TestCase):

    def send_ajax_request(self, data):
        return self.client.get(
            self.url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def validate_recieved_json_response(self, response):
        try:
            return json.loads(response.content)
        except ValueError:
            self.fail('requests view does not return json response content')

    def setUp(self):
        self.url = reverse('requests')

        # We need more than ten requests in for some tests
        for _ in xrange(5):
            Request.objects.create(
                method='GET',
                path='/',
                query='?page=2',
                priority=1
            )
        for _ in xrange(5):
            Request.objects.create(
                method='GET',
                path='/',
                query='',
                priority=0
            )
            Request.objects.create(
                method='GET',
                path='/requests/',
                query='',
                priority=0
            )
        for _ in xrange(5):
            Request.objects.create(
                method='GET',
                path='/',
                query='?page=2',
                priority=1
            )

    def test_requests_view(self):
        '''
        Test my requests view works and uses right templates.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/requests.html', 'hello/base.html']
        )
        self.assertContains(response, 'GET')

        # Assert requests page is linked to index page
        self.assertContains(response, reverse('home'))

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_shows_data_from_db(self):
        '''
        Test my requests view shows data from db on the page.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('requests', response.context)
        self.assertContains(response, 'GET', count=10)
        self.assertContains(response, '/requests/')
        self.assertContains(response, '?page=2')

    def test_requests_view_limits_requests_on_the_page(self):
        '''
        Test there are ten requests on the page.
        '''
        for _ in xrange(10):
            response = self.client.get(self.url)

        self.assertEqual(len(response.context['requests']), 10)

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_handles_ajax_requests(self):
        '''
        Test requests view handles ajax requests, answers with a valid
        json with the right data.
        '''
        response = self.send_ajax_request(dict(id=1))

        self.assertEqual(response.status_code, 200)

        data = self.validate_recieved_json_response(response)

        self.assertIn('new_requests', data)
        self.assertEqual(data['new_requests'], 19)
        self.assertIn('requests', data)
        # data['requests'] is a serialized query set, so I need to
        # turn it into a list
        requests = json.loads(data['requests'])
        self.assertEqual(len(requests), 10)

    def test_requests_view_shows_ten_most_recent_requests(self):
        '''
        Test requests view shows ten most recent requets.
        '''
        for _ in xrange(20):
            self.client.get('home')
        # this response is rendered with 10 previous requests
        response = self.client.get(self.url)
        context_requests = response.context['requests']

        db_requests = Request.objects.all().order_by('-timestamp')
        # Need to convert timestamps because I convert them for requests
        # passed into the context
        for db_request in db_requests:
            db_request.timestamp = to_ecma_date_string(db_request.timestamp)

        for context_request, db_request in zip(context_requests, db_requests):
            self.assertEqual(
                context_request.timestamp,
                db_request.timestamp
            )

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_handles_priority_get_param(self):
        '''
        Test that requests are sorted by priority if there is
        priority=1 in request get params.
        '''
        # Get requests ordered by priority descending
        response = self.client.get(self.url, {'priority': 1})

        self.assertEqual(response.status_code, 200)

        requests = response.context['requests']

        for r in requests:
            self.assertEqual(r.priority, 1)

        # Get requests ordered by priority ascending
        response = self.client.get(self.url, {'priority': 0})

        self.assertEqual(response.status_code, 200)

        requests = response.context['requests']

        for r in requests:
            self.assertEqual(r.priority, 0)

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_handles_ajax_requests_with_priority_param(self):
        '''
        Test that requests view handles ajax requests with priority
        param correctly and sends requests ordered first by priority and
        then by timestamp.
        '''
        # Priority with value 1 == sort by priority descending
        db_requests = Request.objects.all().order_by(
            '-priority', '-timestamp')[:10]

        for db_r in db_requests:
            db_r.timestamp = to_ecma_date_string(db_r.timestamp)

        response = self.send_ajax_request(dict(id=1, priority=1))

        data = self.validate_recieved_json_response(response)

        requests = json.loads(data['requests'])
        for r, db_r in zip(requests, db_requests):
            self.assertEqual(r['fields']['timestamp'], db_r.timestamp)

        db_requests = Request.objects.all().order_by(
            'priority', '-timestamp')[:10]

        for db_r in db_requests:
            db_r.timestamp = to_ecma_date_string(db_r.timestamp)

        response = self.send_ajax_request(dict(id=1, priority=0))

        data = self.validate_recieved_json_response(response)

        requests = json.loads(data['requests'])
        for r, db_r in zip(requests, db_requests):
            self.assertEqual(r['fields']['timestamp'], db_r.timestamp)


class EditFormPageTest(TestCase):

    def setUp(self):
        self.url = reverse('edit_profile')

        User.objects.create_user('test', password='test')
        self.client.login(username='test', password='test')

        Profile.objects.create(
            name='John',
            surname='Snow',
            bio='Bio',
            date_of_birth=datetime.date.today(),
            email='john.snow@mail.com',
            skype='john.snow',
            jabber='john@jabber.com',
            other_contacts='Other contact'
        )

    def test_edit_form_view_displays_form(self):
        '''
        Test that edit form view works, renders the right templates,
        and the response page contains the form.
        '''
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
        self.assertContains(response, 'name="email"')

    def test_edit_profile_page_is_linked_to_home_page(self):
        '''
        Test that edit profile page has a link to the home page.
        '''
        response = self.client.get(self.url)

        # Can't use reverse here for '/'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/"')

    def test_edit_profile_view_renders_template_with_a_form(self):
        '''
        Test that edit_profiel form renders the template with a
        ProfileForm form.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ProfileForm)

    def test_edit_profile_view_populates_form_with_profile_data(self):
        '''
        Test that edit profile form is initially populated with
        profile data from db.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(name='John')

        self.assertContains(response, profile.name)
        self.assertContains(response, profile.surname)
        self.assertContains(response, profile.email)

    def test_edit_profile_view_handles_ajax_post_requests(self):
        '''
        Test that edit profile view updates the profile with recieved
        post data, and stores updated profile to db.
        '''
        response = self.client.post(
            self.url,
            dict(
                name='John',
                surname='Doe',
                bio='Bio',
                date_of_birth='2016-02-18',
                email='john.doe@mail.com',
                jabber='john@jabber.com',
                skype='john.snow',
                other_contacts='Other contacts'
            ),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.get(name='John')
        self.assertEqual(profile.surname, 'Doe')
        self.assertEqual(profile.email, 'john.doe@mail.com')

    def test_edit_profile_view_handles_posts_with_bad_data(self):
        '''
        Test that edit profile view handles invalid recieved post data
        and sends form errors to the client.
        '''
        response = self.client.post(
            self.url,
            dict(
                name='',
                surname='',
                bio='',
                date_of_birth='',
                email=''
            ),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        try:
            errors = json.loads(response.content)
        except ValueError:
            self.fail(
                'edit_profile view returns invalid json '
                'data on bad post data'
            )
        self.assertIn('name', errors)
        self.assertIn('surname', errors)
        self.assertIn('bio', errors)
        self.assertIn('email', errors)
        self.assertIn('date_of_birth', errors)

    def test_access_to_edit_profile_page(self):
        '''
        Test that anonymous user cannot access edit profile page.
        '''
        # Create a new client with no cookies
        self.client = Client()
        response = self.client.get(self.url, follow=True)

        redirect_url, status_code = response.redirect_chain[0]

        self.assertEqual(status_code, 302)
        self.assertEqual(
            redirect_url,
            'http://testserver/login/?next=/edit_profile/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')

    def test_custom_calendar_widget_on_the_edit_profile_page(self):
        '''
        Test that my calendar widget is present on the edit profile page.
        '''
        response = self.client.get(self.url)

        self.assertContains(response, 'datepicker')


class AuthPageTest(TestCase):

    def setUp(self):
        self.url = reverse('login')

    def test_login_view(self):
        '''
        Test login view works and renders the right template.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/login.html', 'hello/base.html']
        )
