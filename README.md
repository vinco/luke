# Luke
Simple scripts and templates for scaffolding a basic Django project


## Prerequisites
+ [Oracle's VirtualBox](https://www.virtualbox.org/)
+ [Vagrant](http://www.vagrantup.com/)
+ [Python](http://www.python.org/)
+ [Fabric](http://www.fabfile.org/)
+ [fabutils](https://github.com/vinco/fabutils)


## Usage
1. Download the repository's tarball and extract it to your project's directory

    ```bash
    $ mkdir myproject
    $ cd myproject
    $ wget https://github.com/vinco/luke/archive/master.tar.gz -O - | tar -xz --strip 1
    ```

2. Set your project's name in `evironments.json`, `fabfile.py` and `provision/provision.sh`

    ```json
    # myproject/environments.json
    {
        "vagrant": {
            "django_settings": "myproject.settings.devel",
        }
    }
    ```

    ```python
    # myproject/fabfile.py
    ...
    # urun('createdb luke -l en_US.UTF-8 -E UTF8 -T template0')
    urun('createdb myproject -l en_US.UTF-8 -E UTF8 -T template0')
    ... 
    # urun('dropdb luke')
    urun('dropdb myproject')
    ...
    ```

    ```bash
    # myproject/provision/provision.sh
    ...
    # PROJECT_NAME=luke
    PROJECT_NAME=myproject
    ...
    ```

3. Create the virtual machine

    ```bash
    $ vagrant up
    ```
4. Redirect the required domains to your localhost
    ```bash
    # /etc/hosts
    192.168.33.2  http://luke.local/
    ```

5. Build the environment inside the virtual machine
    
    ```bash
    $ fab environment:vagrant bootstrap
    ```

6. Run the development server
    
    ```bash
    $ fab environment:vagrant runserver
    ```

7. Init your repository

    ```bash
    $ git init
    ```


# Testing

1. Set your project's name in `tox.ini`.
    
    ```bash
    # change name
    application-import-names = myproject

    DJANGO_SETTINGS_MODULE = myproject.settings.testing

    norecursedirs =
        .*
        src/requirements
        src/myproject/settings
    ```

1. Open vagrant environment from ssh:
    ```bash
    $ vagrant ssh
    ```

2. Change directory to `/vagrant`:
    ```bash
    $ cd /vagrant
    ```

3. Install tox inside the virtual machine:
    ```bash
    $ pip install tox
    ```

4. Run the proper command with tox:

```
# Run the full test suite including the PEP8 linter.
$ tox

# Run only the PEP8 linter.
$ tox -e py27-flake8

# Run only the test suite.
$ tox -e py27-django

# Pass -r flag to recreate the virtual environment when requirements changes.
$ tox -r

# Run the test suite to a specific file.
$ tox -e py27-django src/luke/core/api/tests/test_serializers.py


## Usage API

* To create serializers from luke mixins.
```python
# -*- coding: utf-8 -*-
# luke/application/serializers.py

from rest_framework import serializers

from luke.application.models import Todo

from luke.core.api.serializers import ModelSerializer


class TodoSerializer(ModelSerializer):

    #
    # If your model have a wrong name and you want to change it, only use the
    # property 'source' with the wrong field, after, you put the nice name into
    # fields of your serializer.
    #
    nice_name = serializers.BooleanField(
        source='wrong_name'
    )

    #
    # If you need add a field in your serializer but it is not in your model,
    # you can use SerializerMethodField and this function will search the method
    # name get_name_of_your_field.
    #
    custom_field = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = (
            'id',
            'name',
            'is_active',
            'nice_name',
            'custom_field',
        )

    def get_custom_field(self, instance):
        #
        # Put your code here. 
        #
        return "my custom field"

    #
    # You can rewrite all functions of Django Rest Framework like validate,
    # validate_custom_field, create, update, etc.
    #
    def validate(self, data):
        if not data['is_active']:
            serializers.ValidationError("To do is not active.")

        return data

    def create(self, validated_data):
        todo = Todo(**validated_data)
        todo.save()
        #
        # The actions that you want to do after of save the object.
        #
        

```

* Create a viewset based in luke mixins. With the next code you should can
generate a full API without define the post, get, patch, retrive or delete
functions.
```python
# luke/application/api.py or luke/application/viewsets.py
# -*- coding: utf-8 -*-

from luke.api.v1.routers import router
from luke.application import serializers
from luke.core.api import mixins, viewsets


class TodoViewSet(
        mixins.CreateModelMixin,  # inherit only if you will use create
        mixins.ListModelMixin,  # inherit only if you will use get list
        mixins.DestroyModelMixin,  # inherit only if you will use delete
        mixins.RetrieveModelMixin,  # inherit only if you will get retrive
        mixins.PartialUpdateModelMixin,  # inherit only if you will use patch
        viewsets.GenericViewSet):

    permission_classes = ()

    #
    # Define the general serilizer
    #
    serializer_class = serializers.TodoSerializer

    #
    # Define the serializer wich the app use when the API use Post method.
    #
    create_serializer_class = serializers.TodoSerializer

    #
    # Define the serializer wich the app use when the API use Patch method.
    #
    update_serializer_class = serializers.TodoSerializer

    #
    # Define the serializer wich the app use when the API use Delete method. For
    # example, in this case we didn't define the serializer to this actions, then,
    # the app will use the general serializer.
    #
    destroy_serializer_class = serializers.TodoSerializer

    #
    # Define the serializer wich the app use when the API use Get method without
    # pk in kwargs.
    #
    list_serializer_class = serializers.TodoSerializer

    #
    # Define the serializer wich the app use when the API use Get method without
    # pk in kwargs.
    #
    retrieve_serializer_class = serializers.TodoSerializer

    #
    # You can rewrite the normal functions like get_queryset, get_object ...
    #
    def get_queryset(self):
        self.model.objects.all()


router.register(
    r'todos',
    TodoViewSet,
    base_name="todos"
)

```

* If you need use documentation with swagger, then, you need rewrite the functions
create, update, retrive, etc. And put your documentation after of functions.
```python
# luke/application/api.py or luke/application/viewsets.py
# -*- coding: utf-8 -*-

from luke.api.v1.routers import router
from luke.application import serializers
from luke.core.api import mixins, viewsets


class TodoViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):

    permission_classes = ()

    #
    # Define the general serilizer
    #
    serializer_class = serializers.TodoSerializer
    create_serializer_class = serializers.TodoSerializer
    retrieve_serializer_class = serializers.TodoSerializer

    def create(self, request, *args, **kwargs):
        """
        Allows the session's user to add todo's.
        ---
        request_serializer: serializers.TodoSerializer
        response_serializer: serializers.TodoSerializer

        responseMessages:
            - code: 201
              message: CREATED
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR

        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(TodoViewSet, self).create(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        """
        Allows the session's user get the information for certain todo.
        ---
        request_serializer: serializers.TodoSerializer
        response_serializer: serializers.TodoSerializer

        responseMessages:
            - code: 200
              message: OK
            - code: 404
              message: NOT FOUND
            - code: 400
              message: BAD REQUEST
            - code: 500
              message: INTERNAL SERVER ERROR

        consumes:
            - application/json
        produces:
            - application/json
        """
        return super(TodoViewSet, self).retrieve(request, *args, **kwargs)

    def get_queryset(self):
        self.model.objects.filter(is_active)


router.register(
    r'todos',
    TodoViewSet,
    base_name="todos"
)

```


* If you need nested routes, with mixins is posible.
```python
# luke/application/api.py or luke/application/viewsets.py
# -*- coding: utf-8 -*-

from luke.api.v1.routers import router
from luke.chores import serializers
from luke.core.api import mixins, viewsets


class ChoreViewSet(
        mixins.ListModelMixin,
        viewsets.NestedViewset):

    permission_classes = ()

    serializer_class = serializers.ChoreSerializer
    list_serializer_class = serializers.ChoreSerializer

    def list(self, request, *args, **kwargs):
        return super(ChoreViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        self.model.objects.filter(
            todo=self.kwargs['todo']  # get pk by name defined in the router
        )

#
# The url will be: luke/api/v1/todos/pk/chores
#
router.register_nested(
    r'todos',  # parent prefix
    r'chores',  # prefix
    ChoreViewSet,  # viewset
    parent_lookup_name='todo',  # parent lookup name
    base_name='chores',  # base name
    depth_level=1  # deph level
)

#
# You can change the deph level from 1 - n. By default is 1
#

```

* Also is possible define detail routes.
```python
# luke/application/api.py or luke/application/viewsets.py
# -*- coding: utf-8 -*-

from luke.api.v1.routers import router
from luke.application import serializers
from luke.application.permissions import IsAdminOrIsSelf
from luke.core.api import viewsets

class TodoViewSet(viewsets.GenericViewSet):

    serializer_class = serializers.CustomSerializer
    #
    # Define the serializer of your custom detail_route. The name should be
    # name_of_action_serializer_class.
    #
    custom_action_serializer_class = serializers.CustomSerializer
    
    #
    # You can do custom your detail route. For example, you can define the HHTP
    # method, also, the permission_classes can be defined right here. Finally,
    # if you need that the URL will be different to method name, just you
    # define it in the parameter url_path
    #
    @detail_route(
        methods=['PUT'],
        permission_classes=[IsAdminOrIsSelf],
        url_path='custom-action'
    )
    def custom_action(self, request, *args, **kwars):

        # Serializer that will be used to validate the information.
        update_serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
            action='custom_action'
        )

        update_serializer.is_valid(raise_exception=True)
        serializer = update_serializer.save()

        retrieve_serializer = self.get_serializer(
            serializer,
            action='retrieve'
        )
        return Response(retrieve_serializer.data)

# The url will be: luke/api/v1/todos/custom-action
router.register(
    r'todos',
    TodoViewSet,
    base_name="todos"
)

```
