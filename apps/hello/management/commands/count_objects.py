from django.core.management.base import NoArgsCommand
from django.db import models


class Command(NoArgsCommand):
    help = ('Print to the console number of objects in the '
            'database for all models')

    def handle_noargs(self, *args, **kwargs):
        for model in models.get_models():
            self.stdout.write(
                '{}: {}'.format(model.__name__,
                                model.objects.all().count())
            )
