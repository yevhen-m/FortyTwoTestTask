import os
import json

from django.test import Client
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from apps.hello.models import Profile
from apps.hello.forms import ProfileForm

from ..base_testcase import BaseTestCase


class EditFormPageTest(BaseTestCase):
    fixtures = ['myfixture.json']

    def setUp(self):
        self.url = reverse('edit_profile')

        self.client.login(username='admin', password='admin')

        self.profile_fields = [
            'name',
            'surname',
            'date_of_birth',
            'bio',
            'email',
            'jabber',
            'skype',
            'other_contacts',
            'photo'
        ]

    def test_edit_form_view_displays_form(self):
        '''
        Test edit form view works, renders the right templates,
        and response page contains the form.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/edit_form.html', 'hello/base.html']
        )

        self.assertContains(response, 'editForm')
        for form_field in self.profile_fields:
            self.assertContains(
                response,
                'name="{}"'.format(form_field)
            )

    def test_edit_profile_page_is_linked_to_home_page(self):
        '''
        Test edit profile page has a link to the home page.
        '''
        response = self.client.get(self.url)

        # Can't use reverse here for '/'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/"')

    def test_edit_profile_view_renders_template_with_a_form(self):
        '''
        Test edit_profile view renders the template with a
        ProfileForm form.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ProfileForm)

    def test_edit_profile_view_shows_form_with_profile_data(self):
        '''
        Test that edit profile form is initially populated with
        profile data from db.
        '''
        profile = Profile.objects.first()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        initial_data = response.context['form'].initial

        for field in self.profile_fields:
            self.assertEqual(
                initial_data[field],
                getattr(profile, field)
            )
            if field == 'date_of_birth':
                continue

            self.assertContains(response, getattr(profile, field))

    def test_edit_profile_view_handles_ajax_post_requests(self):
        '''
        Test that edit profile view updates the profile with recieved
        post data, and stores updated profile to db.
        '''
        profile_before_post = Profile.objects.first()

        data = dict(
            name='John',
            surname='Doe',
            bio='John Doe Bio',
            date_of_birth='2006-02-18',
            email='john.doe@mail.com',
            jabber='john@jabber.com',
            skype='john.snow',
            other_contacts='John Doe Contacts'
        )
        response = self.send_ajax_post_request(data)

        self.assertEqual(response.status_code, 200)

        profile_after_post = Profile.objects.first()

        for field in data:
            self.assertNotEqual(
                getattr(profile_after_post, field),
                getattr(profile_before_post, field)
            )
            if field == 'date_of_birth':
                continue

            self.assertEqual(
                getattr(profile_after_post, field),
                data[field]
            )

    def test_edit_profile_view_handles_posts_with_bad_data(self):
        '''
        Test edit profile view handles invalid recieved post data
        and sends form errors to the client.
        '''
        response = self.send_ajax_post_request(dict(
            name='',
            surname='',
            bio='',
            date_of_birth='',
            email=''
        ))

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

    @override_settings(MEDIA_ROOT=BaseTestCase.test_media_root)
    def test_ajax_requests_upload_images_successfully(self):
        '''
        Test that images are uploaded and saved by ajax requests.
        '''
        self.client.login(username='admin', password='admin')

        response = self.client.get(self.url)

        initial_form_data = response.context['form'].initial
        initial_form_data.update(
            photo=self._create_image('test_img.png', (444, 444))
        )

        profile_photo_before_post_request = Profile.objects.first().photo

        response = self.send_ajax_post_request(initial_form_data)

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.first()

        self.assertNotEqual(
            profile.photo,
            profile_photo_before_post_request
        )
        self.assertEqual(
            os.path.basename(profile.photo.name),
            'test_img.png'
        )
