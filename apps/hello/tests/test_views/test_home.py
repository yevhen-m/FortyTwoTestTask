# coding: utf-8

import datetime

from django.test import TestCase
from django.template import Template, Context
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
        the right context and shows all profile data from db.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/index.html', 'hello/base.html']
        )
        self.assertIn('profile', response.context)

        db_profile = Profile.objects.first()
        context_profile = response.context['profile']

        self.assertIsInstance(context_profile, Profile)

        fields = [
            'name',
            'surname',
            'date_of_birth',
            'bio',
            'email',
            'skype',
            'jabber',
            'other_contacts',
            'photo'
        ]
        for field in fields:
            self.assertEqual(
                getattr(context_profile, field),
                getattr(db_profile, field)
            )
            if field == 'date_of_birth':
                continue

            self.assertContains(response, getattr(db_profile, field))

        rendered_date_of_birth = Template('{{ date_of_birth }}').render(
            Context({'date_of_birth': db_profile.date_of_birth})
        )
        self.assertContains(response, rendered_date_of_birth)

    def test_home_page_is_linked_to_requests_page(self):
        '''
        Test home page has a link to requests page.
        '''
        response = self.client.get(self.url)
        # Assert index page is linked to requests page
        self.assertContains(response, reverse('requests'))

    def test_home_page_works_with_no_profiles_in_db(self):
        '''
        Test that my page works with no profile in db.
        '''
        Profile.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_home_page_correctly_works_with_cyrillics(self):
        '''
        Test that cyrillic text is successfully stored in db and shown
        on the page.
        '''
        p = Profile.objects.first()
        p.name = u'Мій'
        p.surname = u'Тест'
        p.skype = u'Скайп'
        p.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        for attr in ('name', 'surname', 'skype'):
            self.assertEqual(
                getattr(response.context['profile'], attr),
                getattr(p, attr)
            )
            self.assertContains(response, getattr(p, attr))

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
        profile = Profile.objects.first()

        response = self.client.get(self.url)
        self.assertContains(
            response,
            reverse('admin:hello_profile_change', args=(profile.pk,))
        )

    def test_data_from_db_is_shown(self):
        '''
        Test that data show on the page is taken from db and is not
        hardcoded into the html page.
        '''
        profile = Profile.objects.first()

        response = self.client.get(self.url)

        self.assertEqual(
            response.context['profile'].name,
            profile.name
        )
        self.assertContains(response, profile.name)

        name, surname = profile.name, profile.surname

        profile.name = 'Jill'
        profile.surname = 'White'
        profile.save()

        self.assertNotEqual(name, profile.name)
        self.assertNotEqual(surname, profile.surname)

        response = self.client.get(self.url)

        self.assertEqual(response.context['profile'].name, 'Jill')
        self.assertEqual(response.context['profile'].surname, 'White')
        self.assertContains(response, 'Jill')
        self.assertContains(response, 'White')
