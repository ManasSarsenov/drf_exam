mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

loaddata:
	python3 manage.py loaddata regions districts

createadmin:
	./manage.py createsuperuser

dumpdata:
	./manage.py dumpdata apps.Category>categories.json
