# Deployment

Constellate uses Postgres and Django, and is designed to be deployable on a modest server.

The steps below outline how to deploy the application:

- using heroku, using their free plans
- using a standard linux private server

## Deploying with heroku

The constellate project describes the required services using an app.json file, which the heroku platform can understand.

If you follow the link below, _in theory_, you can deploy constellate into your own infrastruture just by filling in the required values and hitting "deploy app":

https://dashboard.heroku.com/new?template=https://github.com/Greening-Digital/constellate/tree/master

Sadly, the build process currently times out. If this is still happening when you try to deploy constellate, the manual steps thankfully aren't too complicated tiehreither.

### Create your heroku app

First you'll need to create your heroku application.

Most of the development for constellate is done in Europe, so we'll choose the EU variant, which should run on AWS servers in either Ireland, or Germany:

```
heroku apps:create --region eu your-app
```

Once this is set up, you'll need to be able to push to this new environment. Add a git remote, passing in the name of the app:

```
git remote add your-app "https://git.heroku.com/your-app.git"
```

Heroku knows about your application, and there's now a repositoy you can push to, which will trigger deploys, which will be visible at:

https://your-app.herokuapp.com

We need to set up a database and make it possible to build the front end when deploying though.

### Setup the config

There are a few environment variables you need to set up before you can use constellate, and there are some add-ons.

We need to persist user data, with a database, and we need to add a second buildpack to make it possible to build the Vue frontend for our end users.

#### Add the database

We use PostgresSQL to store state, and it's available for free with heroku. the 10000 row limit should be fine for most constellations.

```
heroku addons:create heroku-postgresql:hobby-dev --app your-app
```

#### Add the buildpacks

The heroku platform has some logic that means it can figure out the kind of application you're using, which can sort out the django part of our deployment.

To build the vue front end though, we need nodejs. The supported way to do this with heroku, is to add a second buildpack, making sure to set the orde,r so that we run the nodejs based steps to build our front end, before trying to serve it:

```
heroku buildpacks:add --index 1 heroku/nodejs --app your-app
heroku buildpacks:add --index 2 heroku/python --app your-app
```

You now should have your buildpacks setup, and you can test this by checking for them on the command line:

```
heroku buildpacks  --app your-app
```

#### Set the environment variables

We're nearly done - we now need to set some environment variables. Copy the sample env file, add the missing values there, like the the credentials for an Amazon S3 storage bucket, we assume you know how to set up a bucket, and make it public readable, and use an account without too many access privileges.

```
# use this for working locally. Some won't necessary
cp sample.env .env

# use this for deployments to your chosne heroku environment.
cp sample.env your-app.env
```

Once you have these, configs setup, you can push them to heroku with `config:push` command.

Conversely, you can pull _from_ heroku with `config:pull`, but for now, our goal is getting the necessary credentials into an environment others can see:

```
heroku config:push --file=your-app.env --app your-app
```

### Deploy

Now that you have:

- the addons for persisting data
- a way to building a pipeline
- a way to build the front end pipeline with the nodejs buildpack
- the necessary environment variables set up


You should be able to deploy with a git push.



```
git push your-app master
```

## Deploying with a regular server

If you have Constellate working locally, then you're halfway to running it on a virtual server.

You need to two things for the change you make to be visible

### Build the front end bundle

There is a make command to create the bundle. You'll need to run this for changes you make to be served by gunicorn, or make changes to serve these static files with apache, nginx, or a similar static file server.

```
make front_end_bundle
```

### Configure gunicorn to serve the application, and a reverse provxy

Next you'll need to serve the application behind an apache or nginx acting as a reverse proxy. Django's [own documentation is on deploying with WSGI/Gunicorn](https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/gunicorn/), is stellar.

It's also worth consulting the procfile to see how gunicorn serves the Constellate app in production.

### Serve the uploaded media files

Constellate assumes that uploaded media is stored on an object store like an AWS S3 bucket or similar. If you are storing the files on your own server, change these lines in `production.py` to use the storage you want to use, as outlined in [django's own extensive documentation on deployment](https://docs.djangoproject.com/en/3.0/howto/deployment/):

```

# MEDIA
# ------------------------------------------------------------------------------
DEFAULT_FILE_STORAGE = "backend.utils.storages.MediaRootS3Boto3Storage"
MEDIA_URL = f"https://{aws_s3_domain}/media/"
```

