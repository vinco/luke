# -*- coding: utf-8 -*-
import sys

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination
)


class ProjectDefaultPagination(PageNumberPagination):
    paginate_by = 24
    paginate_by_param = 'page_size'
    max_paginate_by = 150


class CustomPagination(LimitOffsetPagination):
    """
    Pagination with max value for Integer
    """
    default_limit = sys.maxint
