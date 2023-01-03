# just files are like makefiles but a bit
# more intuitive to use
# https://github.com/casey/just

@test *options:
    pipenv run pytest {{options}}

@ci:
    pipenv run pytest

@serve *options:
    source .venv/bin/activate
    python -m pipenv run python ./manage.py runserver {{options}}

@tailwind-dev:
    python -m pipenv run python ./manage.py tailwind start

@tailwind-build:
    python -m pipenv run python ./manage.py tailwind start

@run *options:
    # run gunicorn in production
    python -m pipenv run gunicorn config.wsgi -b 0.0.0.0:9000 -t 300 {{options}}


