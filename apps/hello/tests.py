from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page(self):
        '''
        Test home page view.
        '''
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('hello/index.html')
        self.assertIn('profile', response.context)
