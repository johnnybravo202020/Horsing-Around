=====
Horsing-Around
=====

Scraps data from the official web site of the horse races run in Turkey, in order to forecast the race results

Quick start
-----------

1. Add "horsing-around" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'horsing-around',
    ]


3. Run `python manage.py migrate` to create the scrapper models if you want to be able to save them.