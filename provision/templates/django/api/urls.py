# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.permissions import AllowAny


urlpatterns = [
    url(
        r'^v1/', include('${PROJECT_NAME}.api.v1.urls', namespace='v1')
    ),
]

if not settings.PRODUCTION:
    schema_view = get_schema_view(
        openapi.Info(
            title="${PROJECT_NAME} API",
            default_version='v1',
            description="API for ${PROJECT_NAME}",
            contact=openapi.Contact(email="python@vincoorbis.com"),
            license=openapi.License(name="BSD License"),
        ),
        validators=['flex'],
        public=True,
        permission_classes=(AllowAny,),
    )
    urlpatterns += [
        url(
            r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=None), name='schema-json'
        ),
        url(
            r'^swagger$',
            schema_view.with_ui('swagger', cache_timeout=None),
            name='schema-swagger-ui'
        ),
        url(
            r'^redoc$',
            schema_view.with_ui('redoc', cache_timeout=None),
            name='schema-redoc'
        ),
    ]