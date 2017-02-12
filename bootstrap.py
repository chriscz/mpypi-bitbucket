from __future__ import print_function
import sys
import os
import signal

from contextlib import contextmanager

import packages as pkgconfig

import mpypi
from mpypi.extension import bitbucket
from mpypi.extension import gitrepo

try:
    import config
except ImportError:
    raise ImportError("did you remember to copy default_config.py to config.py?")

BASEDIR = os.path.dirname(os.path.abspath(__file__))    

class SignalError(RuntimeError): pass

@contextmanager
def pidfile():
    """
    Creates a PID file and deletes it upon return
    """
    pidpath = os.path.join(BASEDIR, 'PID')
    # --- check if it exists
    if os.path.exists(pidpath):
        print("PID file already exists. Not starting Mpypi!", file=sys.stderr)
        sys.exit(1)

    with open(pidpath, 'w') as f:
        f.write(str(os.getpid()))

    defunct = False
    try:
        def sighandler(signal, frame):
            if not defunct:
                msg = "Server killed by signal :: {}".format(signal)
                raise SignalError(msg)
        signal.signal(signal.SIGTERM, sighandler)
        yield
    finally:
        defunct = True
        try:
            os.remove(pidpath)
        except OSError:
            pass

def main():
    username = config.BB_USERNAME
    password = None
    if '-env' in sys.argv:
        username = os.environ['MPYPI_BB_USERNAME']
        password = os.environ['MPYPI_BB_PASSWORD']

    packages = []

    # write PID file
    try:
        with pidfile():
            BITBUCKET = pkgconfig.BITBUCKET + config.BITBUCKET
            GIT_LOCAL = pkgconfig.GIT_LOCAL + config.GIT_LOCAL

            if BITBUCKET:
                bb_pkgs = bitbucket.load_packages(BITBUCKET, username=username, email=config.BB_EMAIL, password=password)
                packages.extend(bb_pkgs)

            if GIT_LOCAL:
                for (package, path) in GIT_LOCAL:
                    with mpypi.cd(BASEDIR):
                        path = os.path.abspath(path)
                    packages.append(gitrepo.GitRepoPackage(package, path, strip_v=True))

            packages.extend(config.EXTRA_PACKAGES)
            mpypi.main(packages, host=config.HOSTNAME, port=config.PORT)
    except SignalError:
        print("mpypi server killed")


if __name__ == '__main__':
    main()
