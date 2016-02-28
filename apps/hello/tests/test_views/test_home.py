# coding: utf-8

import datetime

from django.test import TestCase
from django.core.urlresolvers import reverse

from apps.hello.models import Profile


class HomePageTest(TestCase):
    fixtures = ['myfixture.json']

    def setUp(self):
        self.url = reverse('home')
        Profile.objects.create(
            name='Yevhen',
            surname='Malov',
            date_of_birth=datetime.date.today(),
            bio='My bio',
            email='mail@mail.com',
            skype='skype_id',
            jabber='jabber@jabber.com',
            other_contacts='Other contacts'
        )
        Profile.objects.create(
            name='John',
            surname='Snow',
            date_of_birth=datetime.date.today(),
            bio='Snow bio',
            email='john.snow@mail.com',
            skype='john.snow',
            jabber='john.snow@jabber.com',
            other_contacts='Other contacts'
        )

    def test_home_view(self):
        '''
        Test home page view works, renders the right template with
        the right context and shows my profile data from db.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/index.html', 'hello/base.html']
        )
        self.assertIn('profile', response.context)

        profile = Profile.objects.filter(name='Yevhen')[0]
        c = response.context

        self.assertIsInstance(c['profile'], Profile)
        self.assertEqual(c['profile'].name, profile.name)
        self.assertEqual(c['profile'].surname, profile.surname)

        self.assertContains(response, 'Yevhen')
        self.assertContains(response, 'Malov')
        self.assertContains(response, 'My bio')
        self.assertContains(response, 'yvhn.yvhn@gmail.com')

    def test_home_page_is_linked_to_requests_page(self):
        '''
        Test home page has a link to requests page.
        '''
        response = self.client.get(self.url)
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

    def test_home_page_works_with_two_profiles_in_db(self):
        '''
        Test that my home page works with different profiles in db.
        '''

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yevhen')

    def test_home_page_correctly_works_with_cyrillics(self):
        '''
        Test that home page shows cyrrillic data in the profile.
        '''
        p = Profile.objects.filter(name='Yevhen')[0]
        p.skype = 'Скайп'
        p.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Скайп')

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
        profile = Profile.objects.filter(name='Yevhen')[0]

        response = self.client.get(self.url)
        self.assertContains(response, 'Yevhen')
        self.assertContains(
            response,
            reverse('admin:hello_profile_change', args=(profile.pk,))
        )
