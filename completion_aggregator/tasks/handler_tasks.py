"""
Tasks used in processing signal handlers.
"""

import six
from celery import shared_task
from celery_utils.logged_task import LoggedTask

from django.conf import settings

from ..batch import perform_aggregation
from ..cachegroup import CacheGroup
from ..models import StaleCompletion
from ..utils import get_active_users


@shared_task(task=LoggedTask)
def mark_all_stale(course_key, users=None):
    """
    Mark the specified enrollments as stale for all blocks.
    """
    users = users or get_active_users(course_key)
    stale_objects = [StaleCompletion(username=user.username, course_key=course_key, force=True) for user in users]
    StaleCompletion.objects.bulk_create(stale_objects, batch_size=1000)
    CacheGroup().delete_group(six.text_type(course_key))

    if not getattr(settings, 'COMPLETION_AGGREGATOR_ASYNC_AGGREGATION', False):
        perform_aggregation()
