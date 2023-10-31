# just files are like makefiles but a bit
# more intuitive to use
# https://github.com/casey/just


@test *options:
    python -m pipenv run pytest {{options}}

@install:
    #!/usr/bin/env sh
    python -m pipenv sync 
    cd theme/static_src
    npm install --loglevel error

@ci:
    python -m pipenv run pytest

@serve *options:
    python -m pipenv run python ./manage.py runserver {{options}}

@manage *options:
    python -m pipenv run python ./manage.py {{options}}

@tailwind-dev:
    python -m pipenv run python ./manage.py tailwind start

@tailwind-build:
    python -m pipenv run python ./manage.py tailwind build

@run *options:
    # run gunicorn in production
    python -m pipenv run gunicorn config.wsgi --bind :8000 --workers 2 {{options}}
    # python -m pipenv run gunicorn config.wsgi -b :9000 --timeout 300 {{options}}

@docker-build:
    # create a docker image, tagged as cl8
    docker build . -t cl8

@docker-run:
    # run the current local docker image tagged as cl8, using the env file at .env
    docker run --env-file .env -p 8000:8000 -p 5432:5432 cl8

@caddy:
    caddy run