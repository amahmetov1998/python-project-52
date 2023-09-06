MANAGE := poetry run python manage.py

install:
	@poetry install

make-migration:
	@$(MANAGE) makemigrations

migrate: make-migration
	@$(MANAGE) migrate

build: install migrate

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

dev:
	@$(MANAGE) runserver

PORT ?= 8000
start:
		poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi
