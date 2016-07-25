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