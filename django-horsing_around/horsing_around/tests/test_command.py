import os
import django
from django.conf import settings
from setuptools.command.test import test
from . import django_settings


class TestCommand(test):
    """Django settings will be configured when 'python setup.py test' is run"""
    def run(self):
        # So SQLite db won't be destroyed
        os.environ['REUSE_DB'] = "1"

        settings.configure(BASE_DIR=django_settings.BASE_DIR,
                           TEST_RUNNER=django_settings.TEST_RUNNER,
                           DEBUG=django_settings.DEBUG,
                           INSTALLED_APPS=django_settings.INSTALLED_APPS,
                           DATABASES=django_settings.DATABASES,
                           LOGGING=django_settings.LOGGING)

        from django.core.management import call_command
        django.setup()
        call_command('makemigrations', 'tests')
        call_command('migrate')
        # call_command('shell')
        test.run(self)
