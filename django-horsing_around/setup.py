import os
from setuptools import find_packages, setup

from setuptools.command.test import test


class TestCommand(test):
    """Django settings will be configured when 'python setup.py test' is run"""

    def run(self):
        import django
        from django.conf import settings

        import django_settings
        # So SQLite db won't be destroyed
        os.environ['REUSE_DB'] = "1"

        settings.configure(BASE_DIR=django_settings.BASE_DIR,
                           TEST_RUNNER=django_settings.TEST_RUNNER,
                           DEBUG=django_settings.DEBUG,
                           INSTALLED_APPS=django_settings.INSTALLED_APPS,
                           DATABASES=django_settings.DATABASES,
                           LOGGING=django_settings.LOGGING)

        django.setup()
        test.run(self)


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-horsing_around',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='Scraps data from the official web site of the horse races run in Turkey, in order to forecast the race results',
    long_description=README,
    author='Ege Aydin',
    author_email='egeaydin@gmail.com',
    classifiers=[
        'Environment :: Web or Experimental Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11.4',
        'Intended Audience :: Developers, Data Scientists, Enthusiastic, Bored',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6 - Anaconda 4.3.1',
    ],
    install_requires=[
        'beautifulsoup4',
    ],
    cmdclass={
        'test': TestCommand
    }
)
