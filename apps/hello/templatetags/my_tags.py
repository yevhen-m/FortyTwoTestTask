from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.inclusion_tag('hello/admin_link_url.html')
def admin_link_url(obj):
    try:
        admin_view_name = 'admin:{}_{}_change'.format(
            obj._meta.app_label,
            obj._meta.model_name
        )
        obj_admin_url = reverse(admin_view_name, args=(obj.pk,))
        return dict(object_admin_url=obj_admin_url)
    except AttributeError:
        # obj is None, passed template variable was None
        return {}
