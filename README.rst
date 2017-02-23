Service Book
============

.. image:: http://coveralls.io/repos/github/mozilla/servicebook-web/badge.svg?branch=master
   :target: https://coveralls.io/github/mozilla/servicebook-web?branch=master

.. image:: http://travis-ci.org/mozilla/servicebook-web.svg?branch=master
   :target: https://travis-ci.org/mozilla/servicebook-web


Small dashboard that lists all QA projects, and displays their Swagger
documentation and everything we have about them.


Run with Docker
---------------

There's a full deployment in Docker image in the docker/ directory.

To build it::

    $ cd docker
    $ make docker

Then, to run it::

    $ make run

This will expose the service book on http://localhost:5000

