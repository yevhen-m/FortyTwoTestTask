from django.test import TestCase
from django.template import Template, Context
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


class AdminLinkUrlTagTest(TestCase):

    def test_admin_link_url_tag(self):
        '''
        Test that my custom tag is rendered to correct html when given
        an object.
        '''
        template = Template(
            '{% load my_tags %}'
            '{% admin_link_url object %}'
        )
        bob = get_user_model().objects.create(username='Bob')

        rendered = template.render(Context({'object': bob}))

        link_html = '<a href="{}">Edit (admin)</a>\n'
        self.assertEqual(
            rendered,
            link_html.format(reverse('admin:auth_user_change', args=(bob.pk,)))
        )

    def test_admin_link_url_tag_works_when_passed_none_as_argument(self):
        '''
        Test that my tag handles None as its argument.
        '''
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
