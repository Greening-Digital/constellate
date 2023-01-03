release: python ./manage.py collectstatic --no-input --clear && python ./manage.py migrate

web: gunicorn config.wsgi:application
