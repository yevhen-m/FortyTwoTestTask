from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.hello.models import DBAction


@receiver(post_save)  # noqa
def object_created_or_updated(sender, created, **kwargs):
    if created and sender is not DBAction:
        DBAction.objects.create(
            model=sender.__name__,
            action='created'
        )
    elif sender is not DBAction:
        DBAction.objects.create(
            model=sender.__name__,
            action='updated'
        )


@receiver(post_delete)  # noqa
def object_deleted(sender, **kwargs):
    if sender is not DBAction:
        DBAction.objects.create(
            model=sender.__name__,
            action='deleted'
        )
