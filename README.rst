========
CBVadmin
========

A drop in replacement for Django Admin using django class based views.
The interface made with semantic-ui framework.

The admin uses the following existing django apps.

- django-crispy-forms
- django-filter
- django-simple-menu
- django-tables2

Installing
==========

``pip install cbvadmin``

Add the following to django settings.py

.. code-block:: python

    installed_apps [
        ...
        'cbvadmin',
        'semantic_ui',
        'crispy_forms',
        'django_tables2',
        'django_filters',
        'menu',
    ]
