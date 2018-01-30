# -*- coding: utf-8 -*-
"""
completion_aggregator Django application initialization.
"""

from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class CompletionAggregatorConfig(AppConfig):
    """
    Configuration for the completion_aggregator Django application.
    """

    name = 'completion_aggregator'

    def ready(self):
        """
        Load signal handlers when the app is ready.
        """
        from . import signals as _