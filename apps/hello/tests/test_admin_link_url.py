from django.test import TestCase
from django.template import Template, Context
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


class AdminLinkUrlTagTest(TestCase):

    def test_admin_link_url_tag_renders_to_the_right_link(self):
        template = Template(
            '{% load my_tags %}'
            '{% admin_link_url object %}'
        )
        bob = get_user_model().objects.create(username='Bob')

        rendered = template.render(Context({'object': bob}))

        self.assertEqual(
            rendered,
            reverse('admin:auth_user_change', args=(bob.pk,))
        )
