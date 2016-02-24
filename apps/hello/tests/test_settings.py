from django.test import TestCase
from django.conf import settings


class TestLoginRedirectInSettings(TestCase):

    def test_login_redirect_in_settings(self):
        '''
        Test that I have set proper LOGIN_REDIRECT_URL value.
        '''
        self.assertEqual(
            settings.LOGIN_REDIRECT_URL,
            'home'
        )
