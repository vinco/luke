# -*- coding: utf-8 -*-
def get_query_params(request):
    query_params = {}

    for key, value in request.query_params.iteritems():
        if value.lower() == 'true':
            query_params[key] = True
        elif value.lower() == "false":
            query_params[key] = False
        else:
            query_params[key] = value

    return query_params
