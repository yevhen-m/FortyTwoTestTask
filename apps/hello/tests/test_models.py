from __future__ import division  # noqa
import os
import shutil
from PIL import Image
from StringIO import StringIO

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.conf import settings

from apps.hello.models import Request, Profile


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


class ProfileTest(TestCase):
    fixtures = ['myfixture.json']

    test_media_root = os.path.join(settings.BASE_DIR, '..', 'test_uploads')

    def setUp(self):
        self.url = reverse('edit_profile')

    def tearDown(self):
        shutil.rmtree(self.test_media_root)

    @staticmethod
    def _create_image(name, size):
        file_obj = StringIO()
        file_obj.name = name

        img = Image.new('L', size=size)
        img.save(file_obj, 'png')

        file_obj.seek(0)
        return file_obj

    @override_settings(MEDIA_ROOT=test_media_root)
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

        response = self.client.post(
            self.url,
            initial_form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)

        profile = Profile.objects.first()

        self.assertEqual(max(profile.photo.width, profile.photo.height), 200)
