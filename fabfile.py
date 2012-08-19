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

    with settings(host_string='badger.timeho.me', user='root'):
        exists = run('if [ -d %s ]; then echo TRUE; fi' % env.REMOTE_CODEBASE_PATH) == 'TRUE'

        if not exists:
            run('cd %s && git clone git://github.com/timehome/djangodash2012.git badger' % env.REMOTE_HOME_PATH)
        else:
            run('cd %s && git pull' % env.REMOTE_CODEBASE_PATH)

        run('cd %s && pip install -r requirements.txt' % env.REMOTE_CODEBASE_PATH)

        run('mkdir -p %s/static' % env.REMOTE_HOME_PATH)
        run('cd %s/badger && ./manage.py collectstatic --noinput' % env.REMOTE_CODEBASE_PATH)

    restart()

def db():
    with settings(host_string='badger.timeho.me', user='root'):
        run('mysql -u root --password= -e "DROP DATABASE IF EXISTS badger"')
        run('mysql -u root --password= -e "CREATE DATABASE IF NOT EXISTS badger"')
        run('cd %s/badger && ./manage.py syncdb' % env.REMOTE_CODEBASE_PATH)

def restart():
    with settings(host_string='badger.timeho.me', user='root'):
        for i in range(4):
            run('/etc/init.d/badger-site-80%02d stop && PYTHONPATH=$PYTHONPATH:%s /etc/init.d/badger-site-80%02d start &' % (i, env.REMOTE_CODEBASE_PATH, i))
            run('WORKERNUM=%d /etc/init.d/pyres-worker start' % i)
        run("ps aux | egrep nginx | egrep -v egrep | awk '{ print $2 }' | xargs kill -9")
        run('/etc/init.d/nginx restart')

