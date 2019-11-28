Environment variables
=====================

General settings
----------------

.. envvar:: DATABASE_URL

    Service database connection URL


.. envvar:: AUTHENTICATION_TYPE

    Authentication type can be ``NONE`` or ``TROOD``


.. envvar:: SERVICE_DOMAIN

    Service identification used in TroodCore ecosystem, default ``FILESERVICE``


.. envvar:: SERVICE_AUTH_SECRET

    Random generated string for system token authentication purposes, ``please keep in secret``


.. envvar:: FILES_BASE_URL

    Absolute base URL for files links


.. envvar:: LANGUAGE_CODE

    Default service language


Debug settings
--------------

.. envvar:: DJANGO_CONFIGURATION

    | Service mode, cab be ``Production`` or ``Development``.
    | ``Development`` mode has additional features enabled:
    | - Swagger endpoint at  ``/swagger/``
    

.. envvar:: ENABLE_RAVEN

    Boolean flag for ``Sentry`` logging enabled ``False`` by default
    

.. envvar:: RAVEN_CONFIG_DSN

    Sentry project DSN URL to log events to
    

.. envvar:: RAVEN_CONFIG_RELEASE

    String tag for identify events sent into ``Sentry`` log
    