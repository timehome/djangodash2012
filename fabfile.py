from __future__ import with_statement

import os

from fabric.api import *

env.REMOTE_HOME_PATH = '/home/badger'

env.REMOTE_CODEBASE_PATH = '%s/badger' % env.REMOTE_HOME_PATH

env.PIP_REQUIREMENTS_PATH = 'requirements.txt'

def deploy():
    """
    Full git deployment. Migrations, reloading gunicorn.
    """

    with settings(host_string='50.116.45.155', user='root'):
        exists = run('if [ -d %s ]; then echo TRUE; fi' % env.REMOTE_CODEBASE_PATH) == 'TRUE'

        if not exists:
            run('cd %s && git clone git://github.com/timehome/djangodash2012.git badger' % env.REMOTE_HOME_PATH)
        else:
            run('cd %s && git pull' % env.REMOTE_CODEBASE_PATH)

        run('cd %s && pip install -r requirements.txt' % env.REMOTE_CODEBASE_PATH)
