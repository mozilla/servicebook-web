#!/bin/env/python
import os
from subprocess import call


if __name__ == '__main__':
    travis = 'TRAVIS' in os.environ
    py35 = os.environ.get('TOX_ENV') == 'py35'

    if travis and py35:
        raise SystemExit(call('coveralls'))
