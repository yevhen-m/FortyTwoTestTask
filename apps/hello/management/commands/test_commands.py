from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.db import models


class CountObjectsCommandTest(TestCase):
    fixtures = ['my_test_data.json']

    def test_command_output(self):
        '''
        Test that my command prints number of all objects for all models
        to the console.
        '''
        out = StringIO()
        err = StringIO()

        call_command('count_objects', stdout=out, stderr=err)

        result_out = out.getvalue()
        result_err = err.getvalue()

        for name, number in (
            (m.__name__, m.objects.count()) for m in models.get_models()
        ):
            self.assertIn('{}: {}'.format(name, number), result_out)
            self.assertIn('error: {}: {}'.format(name, number), result_err)
