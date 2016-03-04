from django.db.models.signals import post_save, post_delete
from django.db.utils import OperationalError
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry

from apps.hello.models import DBAction


IGNORED_SENDERS = (DBAction, LogEntry)


def create_DBAction(sender, action):
    try:
        DBAction.objects.create(
            model=sender.__name__,
            action=action
        )
    except OperationalError:
        pass


@receiver(post_save)  # noqa
def object_created_or_updated(sender, created, **kwargs):
    if sender in IGNORED_SENDERS:
        return

    create_DBAction(sender, action=('created' if created else 'updated'))


@receiver(post_delete)  # noqa
def object_deleted(sender, **kwargs):
    if sender in IGNORED_SENDERS:
        return

    create_DBAction(sender, 'deleted')
