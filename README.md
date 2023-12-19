# Constellate - a shared address book for small groups

Constellate is social software designed to help communities of practice and other small-ish groups to discover skills and interests inside the peer group.

By making it easy to identify others with shared interests, or patterns in the make up for skills and knowledge in the community, the goal is make it easier for subgroups to form on new projects, or see where there gaps to bring in new ideas and perspectives.

## Installation

Constellate is a django application, using HTMX for SPA like interactivity.

### Requirements

If you have the following installed:

- a recent version of python 3 (3.11 or higher)
- [pipenv](https://pipenv.pypa.io/) installed
- nodejs 14 or higher
- PostgreSQL

Then you should be able install all the dependencies with one command:

```
just install
```


## Usage

Once you have the necessary environment variables set, you can run the application locally with a single command.

```
just serve
```

You should be able to access the local instance of constellate by visiting:

http://127:0.0.1:8000


## Developing Constellate



### Running tests

```
just test
```

### Contributing

We welcome contributions from code, to translations, to design, documentation, and yes, also feature requests from users.

We use github issues to track public requests, but if you have a private request or query, you can also send an email to constellate@greening.digital.

## License

Constellate is open source, licensed under the Apache 2.0 software license.
