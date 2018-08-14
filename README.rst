Service Book
============

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/mozilla/servicebook-web/blob/master/LICENSE.txt
   :alt: License
.. image:: https://img.shields.io/circleci/project/github/mozilla/servicebook-web/master.svg?logo=circleci
   :alt: CircleCI
   :target: https://circleci.com/gh/mozilla/servicebook/tree/master
.. image:: https://img.shields.io/travis/mozilla/servicebook-web/master.svg?logo=travis
   :target: https://travis-ci.org/mozilla/servicebook-web
   :alt: Travis
.. image:: https://img.shields.io/coveralls/github/mozilla/servicebook-web/master.svg
   :target: https://coveralls.io/github/mozilla/servicebook-web?branch=master
   :alt: Coverage
.. image:: https://pyup.io/repos/github/mozilla/servicebook-web/shield.svg
   :target: https://pyup.io/repos/github/mozilla/servicebook-web/
   :alt: Updates

Small dashboard that lists all QA projects, and displays their Swagger
documentation and everything we have about them.

Hacking on Service Book
-----------------------
By default Service Book will use http://localhost:5000/api/ as the endpoint. If
you want to use something else, you can set the `SERVICEBOOK` environment
variable. For example, set this to http://servicebook.dev.mozaws.net/api/ to
use the development environment. For convenience, you can store this locally in
a `.env` file.

To install the development environment and start Service Book locally::

    $ pipenv install --dev
    $ pipenv run servicebook

Running the tests
~~~~~~~~~~~~~~~~~
To run the tests::

      $ tox

Run with Docker
---------------

There's a full deployment in Docker image.

To build it::

    $ make docker-build

Then, to run it::

    $ make docker-run

This will expose the service book on http://localhost:5000
