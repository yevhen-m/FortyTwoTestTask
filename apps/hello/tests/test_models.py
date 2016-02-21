from django.test import TestCase

from apps.hello.models import Request


class RequestTest(TestCase):

    def test_requests_are_ordered_by_timestamp(self):  # noqa
        kwargs = dict(method='GET',
                      path='/',
                      query='')
        for _ in xrange(3):
            Request.objects.create(**kwargs)

        r1, r2, r3 = Request.objects.all()

        self.assertGreater(r1.timestamp, r2.timestamp)
        self.assertGreater(r2.timestamp, r3.timestamp)
