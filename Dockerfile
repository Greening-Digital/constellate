ARG PYTHON_VERSION=3.11-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

# install node
RUN apt update --yes
RUN apt install curl --yes
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt install --yes build-essential nodejs 


RUN pip install pipenv

COPY Pipfile Pipfile.lock /code/
# RUN pipenv install --production --system
RUN pipenv install --dev --system

COPY . /code
RUN python manage.py tailwind install
RUN python manage.py tailwind build
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "config.wsgi"]
