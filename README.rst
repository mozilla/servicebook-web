Service Book
============

.. image:: http://coveralls.io/repos/github/mozilla/servicebook-web/badge.svg?branch=master
   :target: https://coveralls.io/github/mozilla/servicebook-web?branch=master

.. image:: http://travis-ci.org/mozilla/servicebook-web.svg?branch=master
   :target: https://travis-ci.org/mozilla/servicebook-web


Small dashboard that lists all QA projects, and displays their swagger
documentation and everything we have about them.


Running locally
---------------


To run the Service Book, edit **serviceweb.ini** so
the **service_book** variable in the common section points
to the running Service Book, then:

Create a local virtualenv, install requirements, initialize the DB
then run the service::

    $ virtualenv .
    $ bin/pip install -r requirements.txt
    $ bin/python setup.py develop
    $ bin/serviceweb


Running with Docker
-------------------

Make sure you have a **servicebook/dev** Docker image built in your Docker.
Then Edit **serviceweb.ini** so the **service_book** variable is **http://servicebook:5001/api/**

Last, use docker-compose::

    $ docker-compose up



