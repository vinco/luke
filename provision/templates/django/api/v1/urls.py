# -*- coding: utf-8 -*-
from django.conf.urls import url

from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from .routers import router
from ..autodiscover import autodiscover


autodiscover()

urlpatterns = router.urls + [
    url(
        r'^auth/token-refresh',
        refresh_jwt_token,
        name='auth-token-refresh'
    ),
    url(
        r'^auth/token-verify',
        verify_jwt_token,
        name='auth-token-verify'
    ),
]
