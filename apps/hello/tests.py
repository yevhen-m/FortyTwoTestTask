from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page(self):
        '''
        Test home page view.
        '''
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        # {% extends 'base.html'%} -- index template is loaded first, and the
        # base template is loaded second
        self.assertEqual(
            ['hello/index.html', 'base.html'],
            [t.name for t in response.templates]
        )
        self.assertContains(response, 'Yevhen')
