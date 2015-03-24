# -*- coding: utf-8 -*-
from fabric.api import cd, env, require, run, task
from fabric.context_managers import contextmanager, shell_env

from fabutils import arguments, join, options
from fabutils.tasks import ulocal, urun
from fabutils.env import set_env_from_json_file


@contextmanager
def virtualenv():
    """
    Activates the virtualenv in which the commands shall be run.
    """
    require('site_dir', 'django_settings')

    with cd(env.site_dir):
        with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings):
            yield


@task
def environment(env_name):
    """
    Creates a dynamic environment based on the contents of the given
    environments_file.
    """
    if env_name == 'vagrant':
        result = ulocal('vagrant ssh-config | grep IdentityFile', capture=True)
        env.key_filename = result.split()[1].replace('"', '')

    set_env_from_json_file('environments.json', env_name)


@task
def createdb():
    """
    Creates a new database instance with utf-8 encoding for the project.
    """
    urun('createdb luke -l en_US.UTF-8 -E UTF8 -T template0')


@task
def resetdb():
    """
    Reset the project's database by dropping an creating it again.
    """
    urun('dropdb luke')
    createdb()
    migrate()


@task
def bootstrap():
    """
    Builds the environment to start the project.
    """
    # Build the DB schema and collect the static files.
    createdb()
    migrate()
    collectstatic()


@task
def makemigrations(*args, **kwargs):
    """
    Creates the new migrations based on the project's models changes.
    """
    with virtualenv():
        run(join('python manage.py makemigrations',
                 options(**kwargs), arguments(*args)))


@task
def migrate(*args, **kwargs):
    """
    Syncs the DB and applies the available migrations.
    """
    with virtualenv():
        run(join('python manage.py migrate',
                 options(**kwargs), arguments(*args)))


@task
def collectstatic():
    """
    Collects the static files.
    """
    with virtualenv():
        run('python manage.py collectstatic --noinput')


@task
def runserver():
    """
    Starts the development server inside the Vagrant VM.
    """
    with virtualenv():
        run('python manage.py runserver_plus 0.0.0.0:8000')
