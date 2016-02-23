from django import forms
from django.utils.safestring import mark_safe


class CalendarWidget(forms.DateInput):

    class Media:
        css = {
            'all': (
                'https://code.jquery.com/ui/1.11.3/'
                'themes/smoothness/jquery-ui.css',
            )
        }
        js = (
            'http://code.jquery.com/jquery-1.7.2.min.js',
            'http://code.jquery.com/ui/1.10.2/jquery-ui.js'
        )

    def __init__(self, params=None, attrs=None):
        super(CalendarWidget, self).__init__(attrs=attrs)
        if params is not None:
            # a dict with options for the datepicker
            self.params_str = ', '.join(
                '{}: {}'.format(key, value) for key, value in
                params.iteritems()
            )

    def render(self, name, value, attrs=None):
        rendered = super(CalendarWidget, self).render(
            name, value, attrs=attrs
        )
        script_str = '''
<script>$("#id_{}").datepicker({{{}}});</script>
        '''
        return rendered + mark_safe(script_str.format(name, self.params_str))
