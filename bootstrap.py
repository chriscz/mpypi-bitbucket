from __future__ import print_function
import sys
import os

import mpypi
from mpypi.extension import bitbucket
from packages import PACKAGES

from contextlib import contextmanager

try:
    from config import USERNAME, EMAIL, HOSTNAME, PORT, EXTRA_PACKAGES
except ImportError:
    raise ImportError("did you remember to copy default_config.py to config.py?")



@contextmanager
def pidfile():
    """
    Creates a PID file and deletes it upon return
    """
    BASEDIR = os.path.dirname(os.path.abspath(__file__))    
    pidpath = os.path.join(BASEDIR, 'PID')
    with open(pidpath, 'w') as f:
        f.write(str(os.getpid()))
    yield
    try:
        os.remove(pidpath)
    except OSError:
        pass
    return


def main():
    username = USERNAME
    password = None
    if '-env' in sys.argv:
        username = os.environ['MPYPI_USERNAME']
        password = os.environ['MPYPI_PASSWORD']

    # write PID file
    with pidfile():
        packages = bitbucket.load_packages(PACKAGES, username=username, email=EMAIL, password=password)
        packages.extend(EXTRA_PACKAGES)
        mpypi.main(packages, host=HOSTNAME, port=PORT)


if __name__ == '__main__':
    main()
