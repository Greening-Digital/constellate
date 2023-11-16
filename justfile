# just files are like makefiles but a bit
# more intuitive to use
# https://github.com/casey/just


@test *options:
    pipenv run pytest {{options}}

@install:
    #!/usr/bin/env sh
    pipenv install --dev 
    pipenv run ./manage.py tailwind install
    pipenv run ./manage.py migrate
    pipenv run ./manage.py collectstatic --no-input

@ci:
    pipenv run pytest

@serve *options:
    pipenv run ./manage.py runserver {{options}}

@manage *options:
    pipenv run ./manage.py {{options}}

@tailwind-dev:
    pipenv run ./manage.py tailwind start

@tailwind-build:
    pipenv run ./manage.py tailwind build

@run *options:
    # run gunicorn in production
    pipenv run gunicorn config.wsgi --bind :8000 --workers 2 {{options}}
    # pipenv run gunicorn config.wsgi -b :9000 --timeout 300 {{options}}

@docker-build:
    # create a docker image, tagged as cl8
    docker build . -t cl8

@docker-run:
    # run the current local docker image tagged as cl8, using the env file at .env
    docker run --env-file .env -p 8000:8000 -p 5432:5432 cl8

@caddy:
    caddy run