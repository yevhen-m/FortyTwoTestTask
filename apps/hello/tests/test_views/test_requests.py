import json

from jsrn.datetimeutil import to_ecma_date_string

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from apps.hello.models import Request


class RequestsPageTest(TestCase):

    def send_ajax_request(self, data):
        return self.client.get(
            self.url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def validate_recieved_json_response(self, response):
        try:
            return json.loads(response.content)
        except ValueError:
            self.fail('requests view does not return json response content')

    def setUp(self):
        self.url = reverse('requests')

        # We need more than ten requests in for some tests
        for _ in xrange(5):
            Request.objects.create(
                method='GET',
                path='/',
                query='?page=2',
                priority=1
            )
        for _ in xrange(5):
            Request.objects.create(
                method='GET',
                path='/',
                query='',
                priority=0
            )
            Request.objects.create(
                method='GET',
                path='/requests/',
                query='',
                priority=0
            )
        for _ in xrange(5):
            Request.objects.create(
                method='GET',
                path='/',
                query='?page=2',
                priority=1
            )

    def test_requests_view(self):
        '''
        Test my requests view works and uses right templates.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [t.name for t in response.templates],
            ['hello/requests.html', 'hello/base.html']
        )
        self.assertContains(response, 'GET')

        # Assert requests page is linked to index page
        self.assertContains(response, reverse('home'))

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_shows_data_from_db(self):
        '''
        Test my requests view shows data from db on the page.
        '''
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('requests', response.context)
        self.assertContains(response, 'GET', count=10)
        self.assertContains(response, '/requests/')
        self.assertContains(response, '?page=2')

    def test_requests_view_limits_requests_on_the_page(self):
        '''
        Test there are ten requests on the page.
        '''
        for _ in xrange(10):
            response = self.client.get(self.url)

        self.assertEqual(len(response.context['requests']), 10)

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_handles_ajax_requests(self):
        '''
        Test requests view handles ajax requests, answers with a valid
        json with the right data.
        '''
        response = self.send_ajax_request(dict(id=1))

        self.assertEqual(response.status_code, 200)

        data = self.validate_recieved_json_response(response)

        self.assertIn('new_requests', data)
        self.assertEqual(data['new_requests'], 19)
        self.assertIn('requests', data)
        # data['requests'] is a serialized query set, so I need to
        # turn it into a list
        requests = json.loads(data['requests'])
        self.assertEqual(len(requests), 10)

    def test_requests_view_shows_ten_most_recent_requests(self):
        '''
        Test requests view shows ten most recent requets.
        '''
        for _ in xrange(20):
            self.client.get('home')
        # this response is rendered with 10 previous requests
        response = self.client.get(self.url)
        context_requests = response.context['requests']

        db_requests = Request.objects.all().order_by('-timestamp')
        # Need to convert timestamps because I convert them for requests
        # passed into the context
        for db_request in db_requests:
            db_request.timestamp = to_ecma_date_string(db_request.timestamp)

        for context_request, db_request in zip(context_requests, db_requests):
            self.assertEqual(
                context_request.timestamp,
                db_request.timestamp
            )

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_handles_priority_get_param(self):
        '''
        Test that requests are sorted by priority if there is
        priority=1 in request get params.
        '''
        # Get requests ordered by priority descending
        response = self.client.get(self.url, {'priority': 1})

        self.assertEqual(response.status_code, 200)

        requests = response.context['requests']

        for r in requests:
            self.assertEqual(r.priority, 1)

        # Get requests ordered by priority ascending
        response = self.client.get(self.url, {'priority': 0})

        self.assertEqual(response.status_code, 200)

        requests = response.context['requests']

        for r in requests:
            self.assertEqual(r.priority, 0)

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_requests_view_handles_ajax_requests_with_priority_param(self):
        '''
        Test that requests view handles ajax requests with priority
        param correctly and sends requests ordered first by priority and
        then by timestamp.
        '''
        # Priority with value 1 == sort by priority descending
        db_requests = Request.objects.all().order_by(
            '-priority', '-timestamp')[:10]

        for db_r in db_requests:
            db_r.timestamp = to_ecma_date_string(db_r.timestamp)

        response = self.send_ajax_request(dict(id=1, priority=1))

        data = self.validate_recieved_json_response(response)

        requests = json.loads(data['requests'])
        for r, db_r in zip(requests, db_requests):
            self.assertEqual(r['fields']['timestamp'], db_r.timestamp)

        db_requests = Request.objects.all().order_by(
            'priority', '-timestamp')[:10]

        for db_r in db_requests:
            db_r.timestamp = to_ecma_date_string(db_r.timestamp)

        response = self.send_ajax_request(dict(id=1, priority=0))

        data = self.validate_recieved_json_response(response)

        requests = json.loads(data['requests'])
        for r, db_r in zip(requests, db_requests):
            self.assertEqual(r['fields']['timestamp'], db_r.timestamp)
