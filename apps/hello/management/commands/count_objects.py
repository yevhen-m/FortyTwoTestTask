from django.core.management.base import NoArgsCommand
from django.db import models


class Command(NoArgsCommand):
    help = ('Print to the console number of objects in the '
            'database for all models')

    def handle_noargs(self, *args, **kwargs):
        out_str = '{}: {}'
        err_str = 'error: {}: {}'

        for name, number in (
                (m.__name__, m.objects.count()) for m in models.get_models()
        ):
            self.stdout.write(out_str.format(name, number))
            self.stderr.write(err_str.format(name, number))
