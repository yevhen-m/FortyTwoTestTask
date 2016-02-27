import datetime

from django.test import TestCase

from apps.hello.models import Request, DBAction


class SignalTest(TestCase):

    def setUp(self):
        Request.objects.create(
            method='GET',
            path='/',
            query='',
            timestamp=datetime.datetime.now()
        )

    def test_db_action_signal_handler_deals_with_objects_creation(self):
        '''
        Test that my signal handler stores data about objects creation
        to db.
        '''
        db_action = DBAction.objects.last()

        self.assertEqual(db_action.model, 'Request')
        self.assertEqual(db_action.action, 'created')

    def test_db_action_signal_handler_deals_with_objects_editing(self):
        '''
        Test that my handler handles objects editing.
        '''
        request = Request.objects.last()
        request.method = 'POST'
        request.save()

        db_action = DBAction.objects.last()

        self.assertEqual(db_action.model, 'Request')
        self.assertEqual(db_action.action, 'updated')

    def test_db_action_signal_handler_deals_with_object_deletion(self):
        '''
        Test that my handler handles post_delete signal.
        '''
        request = Request.objects.first()
        request.delete()

        db_action = DBAction.objects.last()

        self.assertEqual(db_action.model, 'Request')
        self.assertEqual(db_action.action, 'deleted')

    def test_my_signal_handlers_do_not_save_data_about_themselves(self):
        '''
        Test that my handlers don't save data about DBAction objects.
        '''
        DBAction.objects.create(
            model=DBAction.__name__,
            action='test_created',
        )
        db_action1, db_action2 = DBAction.objects.all().order_by(
            '-timestamp')[:2]

        # db_action1 should be DBAction object created in this test
        self.assertEqual(db_action1.model, DBAction.__name__)
        self.assertEqual(db_action1.action, 'test_created')

        # db_action2 object is for Request creation in setUp method
        self.assertEqual(db_action2.model, Request.__name__)
        self.assertEqual(db_action2.action, 'created')
