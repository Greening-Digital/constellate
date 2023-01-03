# just files are like makefiles but a bit
# more intuitive to
# https://github.com/casey/just

@test *options:
    pipenv run pytest {{options}}

@server *options:
    python -m pipenv run python ./manage.py runserver {{options}}

