# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class CreateModelMixin(object):
    """
    Create a model instance.
    """
    def create(self, request, *args, **kwargs):
        # Serializer that will be used to create the object.
        data = request.data

        # Pass kwargs to data
        if kwargs:
            for key, value in kwargs.iteritems():
                data.update({key: value})

        # Serializer that will be used to create the object.
        create_serializer = self.get_serializer(
            data=data,
            action='create'
            )
        create_serializer.is_valid(raise_exception=True)
        created_object = self.perform_create(create_serializer)

        # Serializer that will be used to retrieve the object.
        retrieve_serializer = self.get_serializer(
            created_object,
            action='retrieve'
        )
        headers = self.get_success_headers(retrieve_serializer.data)
        return Response(
            retrieve_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, action='list')
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin(object):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, action='retrieve')
        return Response(serializer.data)


class UpdateModelMixin(object):
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Serializer that will be used to update the object.
        update_serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=False,
            action='update'
        )
        update_serializer.is_valid(raise_exception=True)
        updated_object = update_serializer.save()

        # Serializer that will be used to retrieve the object.
        retrieve_serializer = self.get_serializer(
            updated_object,
            action='retrieve'
        )
        return Response(retrieve_serializer.data)


class PartialUpdateModelMixin(object):
    """
    Update a model instance (partially).
    """
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Serializer that will be used to update the object.
        update_serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True,
            action='update'
        )
        update_serializer.is_valid(raise_exception=True)
        updated_object = update_serializer.save()

        # Serializer that will be used to retrieve the object.
        retrieve_serializer = self.get_serializer(
            updated_object,
            action='retrieve'
        )
        return Response(retrieve_serializer.data)


class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
