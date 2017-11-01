import os
from setuptools import find_packages, setup
from horsing_around.tests.test_command import TestCommand

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-horsing_around',
    version='0.1.3',
    packages=find_packages(exclude=("tests",)),
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
