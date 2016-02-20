from django.test import TestCase

from .models import Profile


class HomePageTest(TestCase):
    fixtures = ['myfixture.json']

    def test_home_page(self):
        '''
        Test home page view.
        '''
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('hello/index.html')
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


class RequestsTest(TestCase):

    def test_requests_page(self):
        response = self.client.get('/requests/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('hello/requests.html')
        self.assertContains(response, 'GET')
