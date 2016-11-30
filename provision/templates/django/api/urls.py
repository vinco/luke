# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url


urlpatterns = [
    url(
        r'^v1/', include('redsep.api.v1.urls', namespace='v1')
    ),
]

if not settings.PRODUCTION:
    urlpatterns += [
        url(
            r'^docs/', include('rest_framework_swagger.urls')
        ),
    ]
