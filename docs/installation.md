# Installation

Constellate is made of two parts - a django API in `backend`, and a VueJS front end in `frontend`.

You need them both running to develop the site.


### Setting up the django backend

While you almost definitely should be using postgres in development and production to avoid surprises during deployment.

But you CAN use sqlite to spin up an instance and try it out. Pass in a database url string like the one below:

```python
# backend/config/local.py
DATABASE_URL="sqlite:///backend_db"
```

Once this is updated ou can run `heroku local web` to run gunicorn, or for an auto-reloading dev server, run `python ./manage.py runserver`.

For the `runserver`, you will need to load the environment variables listed in `.env` into your shell.


### Set up the front end

The front end is a VueJS application, that talks to the backend. Like a lot of VueJS apps you can install using npm or yarn.

The examples below use npm for brevity.

```

npm install
```

Once you have that, for development call `npm run serve` - this sets up hot reloading, and development server:

```
npm run serve
```

To create a build for production with `npm run build`. This creates an optimised version to deploy onto your choice of static hosting.

You can see the changes made to the config in the `vue.config.js` to get the vue app working as a single deployable unit with Django.


```
npm run build
```
