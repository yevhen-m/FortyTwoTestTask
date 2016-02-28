from django.test import TestCase
from django.core.urlresolvers import reverse


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
