# Deployment

Constellate uses PostgresSQL and Django, and is designed to be deployable on a modest server.

The steps below outline how to deploy the application:

- using a standard linux private server

## Deploying with a regular server

If you have Constellate working locally, then you're halfway to running it on a virtual server.

### Build the front end bundle

There is a make command to create the bundle. You'll need to run this for changes you make to be served by gunicorn, or make changes to serve these static files with apache, nginx, or a similar static file server.

```
just tailwind-build
```

### Configure gunicorn to serve the application, and a reverse provxy

Next you'll need to serve the application behind an apache or nginx acting as a reverse proxy. Django's [own documentation is on deploying with WSGI/Gunicorn](https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/gunicorn/), is stellar.


### Serve the uploaded media files

Constellate assumes that uploaded media is stored on an object store like an AWS S3 bucket or similar. If you are storing the files on your own server, change these lines in `production.py` to use the storage you want to use, as outlined in [django's own extensive documentation on deployment](https://docs.djangoproject.com/en/3.0/howto/deployment/):

```

# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "cl8.utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{aws_s3_domain}/media/"
```

