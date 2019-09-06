Files service
===========



Quickstart
----------

Start TroodFiles service container:

```
docker run -d -p 127.0.0.1:8000:8000/tcp \
    --env DJANGO_CONFIGURATION=Development \
    --env AUTH_TYPE=NONE \
    --env DATABASE_URL=sqlite://./db.sqlite3 \
    --name=fileservice registry.tools.trood.ru/files:dev
```

Initiate database structure for created container:

```
docker exec fileservice python manage.py migrate
```

Upload your first File:

```

```

Check other API methods on documentation:

```
open http://127.0.0.1:8000/swagger/
```



Contents
--------

.. toctree::
   :maxdepth: 2
   :glob:

   get-started
   rest-api
   autoapi/index