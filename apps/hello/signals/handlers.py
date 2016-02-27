from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.hello.models import DBAction


@receiver(post_save)  # noqa
def object_created(sender, created, **kwargs):
    if created and sender is not DBAction:
        DBAction.objects.create(
            model=sender.__name__,
            action='created'
        )
