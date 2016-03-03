from django.db.models.signals import post_save, post_delete
from django.db.utils import OperationalError
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry

from apps.hello.models import DBAction


IGNORED_SENDERS = (DBAction, LogEntry)


@receiver(post_save)  # noqa
def object_created_or_updated(sender, created, **kwargs):
    if created and sender not in IGNORED_SENDERS:
        try:
            DBAction.objects.create(
                model=sender.__name__,
                action='created'
            )
        except OperationalError:
            pass
    elif sender not in IGNORED_SENDERS:
        try:
            DBAction.objects.create(
                model=sender.__name__,
                action='updated'
            )
        except OperationalError:
            pass


@receiver(post_delete)  # noqa
def object_deleted(sender, **kwargs):
    if sender not in IGNORED_SENDERS:
        try:
            DBAction.objects.create(
                model=sender.__name__,
                action='deleted'
            )
        except OperationalError:
            pass
