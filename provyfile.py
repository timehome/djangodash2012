#!/usr/bin/python
# -*- coding: utf-8 -*-

from provy.core import Role, AskFor
from provy.more.debian import UserRole, DjangoRole, SupervisorRole, NginxRole, MySQLRole, PipRole, AptitudeRole

class FrontEnd(Role):
    def provision(self):
        user_pass = self.context['user-pass']

        with self.using(UserRole) as role:
            role.ensure_user('badger', identified_by=user_pass, is_admin=False)

        with self.using(AptitudeRole) as role:
            role.ensure_package_installed('git-core')
            role.ensure_package_installed('cmake')

        with self.using(NginxRole) as role:
            role.ensure_conf(conf_template='nginx.conf', options={'user': 'badger'})
            role.ensure_site_disabled('default')
            role.create_site(site='website', template='website')
            role.ensure_site_enabled('website')

        with self.using(MySQLRole) as role:
            role.ensure_user(username='badger',
                             identified_by=self.context['mysql-pass'])

            role.ensure_database('badger'),
            role.ensure_grant('ALL PRIVILEGES',
                on='badger.*',
                username='badger',
                login_from='%',
                with_grant_option=True)


        self.provision_role(PipRole) # does not need to be called if using with block.

        with self.using(SupervisorRole) as role:
            role.config(
                config_file_directory='/home/badger',
                pidfile='/home/badger/supervisor.pid',
                log_folder='/home/badger',
                user='badger'
            )

            with self.using(DjangoRole) as role:
                role.restart_supervisor_on_changes = True

                with role.create_site('badger-site') as site:
                    site.settings_path = '/home/badger/badger/badger.settings'
                    site.pid_file_path = '/home/badger'
                    site.use_supervisor = True
                    site.supervisor_log_path = '/home/badger/'
                    site.threads = 4
                    site.processes = 4
                    site.user = 'badger'

                    # settings that override the website defaults.
                    site.settings = {
                        'DATABASES': {
                            'default': {
                                'ENGINE': 'django.db.backends.mysql',
                                'NAME': 'badger',
                                'USER': 'badger',
                                'PASSWORD': self.context['mysql-pass'],
                                'HOST': '',
                                'PORT': ''
                            }
                        }
                    }

servers = {
    'badger': {
        'frontend': {
            'address': 'badger.timeho.me',
            'user': 'root',
            'roles': [
                FrontEnd
            ],
            'options': {
                'user-pass': AskFor('user-pass', 'Please enter the password for the server user'),
                'mysql-pass': AskFor('mysql-pass', 'Please enter the password for the mysql user')
            }
        }
    }
}
