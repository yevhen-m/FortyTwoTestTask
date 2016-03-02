from __future__ import division  # noqa

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from apps.hello.models import Request, Profile

from .base_testcase import BaseTestCase


class RequestTest(TestCase):

    def test_requests_are_ordered_by_timestamp(self):
        '''
        Test that Request default querysets are ordered by timestamp
        descending.
        '''
        kwargs = dict(method='GET',
                      path='/',
                      query='')
        for _ in xrange(3):
            Request.objects.create(**kwargs)

        r1, r2, r3 = Request.objects.all()

        self.assertGreater(r1.timestamp, r2.timestamp)
        self.assertGreater(r2.timestamp, r3.timestamp)


class ProfileTest(BaseTestCase):
    fixtures = ['myfixture.json']

    def setUp(self):
        self.url = reverse('edit_profile')

    @override_settings(MEDIA_ROOT=BaseTestCase.test_media_root)
    def test_uploaded_images_are_resized_properly(self):
        '''
        Test that uploaded form edit profile form page images are
        resized properly on the server side.
        '''
        self.client.login(username='admin', password='admin')

        response = self.client.get(self.url)

        initial_form_data = response.context['form'].initial
        initial_form_data.update(
            photo=self._create_image('test_img.png', (444, 444))
        )

        response = self.send_ajax_post_request(initial_form_data)

        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.first()

        self.assertEqual(max(profile.photo.width, profile.photo.height), 200)

    @override_settings(MEDIA_ROOT=BaseTestCase.test_media_root)
    def test_uploaded_images_have_the_same_ratio(self):
        '''
        Test images have the same ratio after they get resized.
        '''
        self.client.login(username='admin', password='admin')

        response = self.client.get(self.url)

        initial_form_data = response.context['form'].initial

        for width, height in (
                (100, 800),
                (800, 100),
                (100, 100),
                (999, 999)
        ):
            initial_photo_ratio = width / height

            initial_form_data.update(
                photo=self._create_image('test_img.png', (width, height))
            )

            response = self.send_ajax_post_request(initial_form_data)

            self.assertEqual(response.status_code, 200)

            profile = Profile.objects.first()
            resized_photo_ratio = profile.photo.width / profile.photo.height

            self.assertAlmostEqual(initial_photo_ratio, resized_photo_ratio)
