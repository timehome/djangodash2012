run:
	@cd badger && DJANGO_SETTINGS_MODULE=badger.settings_local ./manage.py runserver 0.0.0.0:8000

db:
	@mysql -u root -e 'DROP DATABASE IF EXISTS badger'
	@mysql -u root -e 'CREATE DATABASE IF NOT EXISTS badger'
	@cd badger && ./manage.py syncdb

# %%%%%%%%%%%%%% REDIS %%%%%%%%%%%%%%
kill_redis:
	@ps aux | awk '(/redis-server/ && $$0 !~ /awk/){ system("kill -9 "$$2) }'

redis: kill_redis
	@mkdir -p /tmp/badger/db
	@redis-server redis.conf &

run_worker:
	@cd badger && PYTHONPATH=.:$$PYTHONPATH DJANGO_SETTINGS_MODULE=badger.settings pyres_worker repo_queue

run_worker_prod:
	@cd /home/badger/badger/badger && PYTHONPATH=/home/badger/badger:$$PYTHONPATH DJANGO_SETTINGS_MODULE=badger.settings pyres_worker -f /home/badger/worker.log repo_queue
