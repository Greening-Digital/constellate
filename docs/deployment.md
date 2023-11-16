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

In production, Constellate assumes that uploaded media is stored on an object store like an AWS S3 bucket or similar. 

If you are storing the files on a local file system, and storing files on the same server as the running application  running comment out the entire `STORAGES` stanza of `production.py` 

For more, see [django's own extensive documentation on deployment](https://docs.djangoproject.com/en/3.0/howto/deployment/).
```





