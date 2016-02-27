import datetime

from django.test import TestCase

from apps.hello.models import Request, DBAction


class SignalTest(TestCase):

    def test_db_action_signal_handler(self):
        '''
        Test that my signal handlers stores objects creation to db.
        '''
        timestamp = datetime.datetime.now()

        Request.objects.create(
            method='GET',
            path='/',
            query='',
            timestamp=timestamp
        )

        db_action = DBAction.objects.last()

        self.assertEqual(db_action.method, 'GET')
        self.assertEqual(db_action.path, '/')
        self.assertEqual(db_action.query, '')
        self.assertEqual(db_action.timestamp, timestamp)
