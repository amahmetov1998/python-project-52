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
	poetry run coverage xml --include=* --omit=task_manager/settings.py