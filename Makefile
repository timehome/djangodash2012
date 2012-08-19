run:
	@cd badger && DJANGO_SETTINGS_MODULE=badger.settings_local ./manage.py runserver 0.0.0.0:8000

db:
	@mysql -u root -e 'CREATE DATABASE IF NOT EXISTS badger'
	@cd badger && ./manage.py syncdb

run_worker:
	@PYTHONPATH=.:$$PYTHONPATH && cd badger && DJANGO_SETTINGS_MODULE=badger.settings pyres_worker repo_queue

run_worker_prod:
	@PYTHONPATH=/home/badger/badger:$$PYTHONPATH && cd /home/badger/badger/badger && DJANGO_SETTINGS_MODULE=badger.settings pyres_worker -f /home/badger/worker.log repo_queue
