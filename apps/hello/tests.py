from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            ['base.html', 'hello/index.html'],
            [t.name for t in response.templates]
        )
        self.assertContains(response, 'Yevhen')
