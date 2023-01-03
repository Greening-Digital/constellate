# just files are like makefiles but a bit
# more intuitive to
# https://github.com/casey/just

@test *options:
    cd backend && \
    pipenv run pytest {{options}}

@server *options:
    cd backend && \
    python -m pipenv run python ./manage.py runserver {{options}}
