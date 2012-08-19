run:
	@cd badger && ./manage.py runserver 0.0.0.0:8000

db:
	@mysql -u root -e 'CREATE DATABASE IF NOT EXISTS badger'
	@cd badger && ./manage.py syncdb

run_worker:
	@PYTHONPATH=.:$$PYTHONPATH && cd badger && DJANGO_SETTINGS_MODULE=badger.settings pyres_worker repo_queue
