from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.db import models

from apps.hello.models import Profile, Request
from django.contrib.auth.models import User


class CountObjectsCommandTest(TestCase):
    fixtures = ['my_test_data.json']

    def test_command_output(self):
        '''
        Test that my command prints number of all objects for all models
        to the console.
        '''
        out = StringIO()

        call_command('count_objects', stdout=out)

        result = out.getvalue()

        profiles_number = Profile.objects.all().count()
        requests_number = Request.objects.all().count()
        users_number = User.objects.all().count()

        self.assertIn('Profile: {}'.format(profiles_number), result)
        self.assertIn('Request: {}'.format(requests_number), result)
        self.assertIn('User: {}'.format(users_number), result)

        for name in (m.__name__ for m in models.get_models()):
            self.assertIn(name, result)
