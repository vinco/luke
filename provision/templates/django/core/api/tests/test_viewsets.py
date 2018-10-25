# -*- coding: utf-8 -*-
from rest_framework_jwt.settings import api_settings

class ApiTestMixin(object):
    """
    Common operations for API testing
    """

    def create_token(self, user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        return 'JWT {0}'.format(jwt_encode_handler(payload))
