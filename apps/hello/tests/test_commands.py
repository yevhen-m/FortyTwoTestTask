from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.db import models


class CountObjectsCommandTest(TestCase):
    fixtures = ['my_test_data.json']

    def test_command_output(self):
        out = StringIO()

        call_command('count_objects', stdout=out)

        result = out.getvalue()

        self.assertIn('Profile: 2', result)
        self.assertIn('Request: 1096', result)
        self.assertIn('User: 1', result)

        for name in (m.__name__ for m in models.get_models()):
            self.assertIn(name, result)
