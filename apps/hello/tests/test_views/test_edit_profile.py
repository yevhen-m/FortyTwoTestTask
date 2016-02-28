import json
import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.hello.models import Profile
from apps.hello.forms import ProfileForm


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
