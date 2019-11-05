Files service
=============



Quickstart
----------

Download and start TroodFiles service container:

.. code-block:: bash

    docker pull registry.tools.trood.ru/files:dev
    docker run -d -p 127.0.0.1:8000:8000/tcp \
        --env DJANGO_CONFIGURATION=Development \
        --env AUTH_TYPE=NONE \
        --env DATABASE_URL=sqlite://./db.sqlite3 \
        --name=fileservice registry.tools.trood.ru/files:dev


Initiate database structure for created container:

.. code-block:: bash

    docker exec fileservice python manage.py migrate


Upload your first File:

.. code-block:: bash

    curl -X POST 'http://127.0.0.1:8000/api/v1.0/files/' \
        -F 'name=My test file' \
        -F 'file=@./test.jpg'


Check other API methods on documentation:

.. code-block:: bash

    open http://127.0.0.1:8000/swagger/



Contents
--------

.. toctree::
   :maxdepth: 2
   :glob:

   config
   rest-api
   autoapi/index