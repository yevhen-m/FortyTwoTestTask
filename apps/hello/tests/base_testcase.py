import os
import shutil
from PIL import Image
from StringIO import StringIO
from django.test import TestCase
from django.conf import settings


class BaseTestCase(TestCase):

    test_media_root = os.path.join(settings.BASE_DIR, '..', 'test_uploads')

    def tearDown(self):
        try:
            shutil.rmtree(self.test_media_root)
        except OSError:
            pass

    @staticmethod
    def _create_image(name, size):
        file_obj = StringIO()
        file_obj.name = name

        img = Image.new('L', size=size)
        img.save(file_obj, 'png')

        file_obj.seek(0)
        return file_obj

    def send_ajax_post_request(self, data):
        return self.client.post(
            self.url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
