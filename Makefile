mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	python3 manage.py ram

ram:
	python3 manage.py ram

admin:
	python3 manage.py createsuperuser --noinput

remig:
	make unmig
	make ram
	make mig
	make admin

search_index:
	python3 manage.py search_index --rebuild
