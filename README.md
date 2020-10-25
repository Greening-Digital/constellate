# Constellate - a shared address book for small groups

Constellate is social software designed to help communities of practice and other small-ish groups to discover skills and interests inside the peer group.

By making it easy to identify others with shared interests, or patters in the make up for skills and knowledge in the community, the goal is make it easier for subgroups to form on new projects, or see where there gaps to bring in new ideas abd perspectives.

## Installation

Constellate is made of two parts - a VueJS front end, that most users see, that connects to a Django API backend, with an admin interface used by administrators and moderators.

### Requirements

If you have the following installed:

- a recent version of python 3 (3.6 or higher)
- [pipenv](https://pipenv.pypa.io/) installed
- nodejs 10 or higher
- PostgreSQL

Then you should be able install all the dependencies with one command:

```
make install
```


### In more detail - installing the backend:

As mentioned before, the backend of Constellate is a django project, using Django Request Framework to manage sign-in, authentication, and provide a JSON API for the front end to consumer.

It relies on pipenv for managing depencies and environment variables, and all the required environment variables are outlined in `sample.env`, in the project root.

If you don't want to use make, you can call `pipenv install` inside the `backend` directory, but you will still need to call `pipenv shell` in the project root to load the correct environment variables into the shell.

### Install the front end

The front end is a [Vue 2.x](https://vuejs.org/) app, using [Vuex](https://vuex.vuejs.org/) for managing state.

If you don't want to use make, you can install it by running npm install in the project root.

```
npm install
```

You'll need them both running to develop the site, and a few environment variables set.

See `sample.env` for a full list of the required variables.

By default, the production environment assumes deployment to heroku, using an external mail service like mailgun, and object storage like Amazon S3 for storing uploaded files, and serving most static files with whitenoise.

If you prefer, you can run this anywhere that can run a django application and postgres, although you will need to use a service like nginx or traefik to serve uploaded media.

## Usage

Once you have the necessary environment variables set, you can run the application locally with a single command.

```
make serve
```

This will:

- make a compiled version of the front end Vue JS application
- copy the main template to a directory where the django app can serve it
- copy accross any other front end assets generated as part of the build process
- serve the application on localhost, port 8000

You should be able to access the local instance of constellate by visiting:

http://127:0.0.1:8000


## Developing Constellate

Assuming you have:

- the correct environment variables set
- a database setup
- installed the necessary dependencies for javascript and python


Then you can run the front and backend separately, for easier development.

Start the backend by itself with:

```
make dev.backend
```

This will setup a django dev server, that by default runs on at 127.0.0.1 and port 8000.


Start the front end with:


```
make dev.frontend
```

This will set up a hot reloading server, serving the vue front end at http://127.0.0.1:8080, and proxying API requests to the backend, to simulate the two services being run on a single machine in production.

### Running tests

The front end of constellate uses jest for tests. Calling `make test.frontend` uses the `vue-cli-service` to run tests with a special config to account for the project layout

```
make test.frontend
```

The backend of constellate uses pytest for testing the API. Call `make test.backend` to run pytest in the `backend` directory.

### Contributing

We welcome contributions from code, to translations, to design, documentation, and yes, also feature requests from users.

We use github issues to track public requests, but if you have a private request or query, you can also send an email to constellate@greening.digital.

## License

Constellate is open source, licensed under the Apache 2.0 software license.
