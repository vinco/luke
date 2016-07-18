# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedMixin(models.Model):
    """
    Abstract model that defines the auto populated 'created_date' and
    'last_modified' fields.

    This model must be used as the base for all the models in the project.
    """
    created_date = models.DateTimeField(
        editable=False,
        blank=True, null=True,
        auto_now_add=True,
        verbose_name=_('created date')
    )
    last_modified = models.DateTimeField(
        editable=False,
        blank=True, null=True,
        auto_now=True,
        verbose_name=_('last modified'),
    )

    class Meta:
        abstract = True
