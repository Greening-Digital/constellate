# Installation

Constellate is a Django application, that connects to a Postgres database.
It also relies on a front end toolchain, Tailwind for generating minimal CSS, and on MJML generating the markup for sent emails.

While you can run commands directly, it's also easier to use just for running commands, to avoid needing to remember 
each invocation. Download it from - https://just.systems

### Setting up your server 

#### Create or connect to an existing a database

```
createdb yourdatabase_cl8
```

Once you have the database set up, you'll need to list it in your .env file. You should consult .env.sample 
for explanations of all the settings listed, for now, add the database name into your database connection string like below.

```
# .env
DATABASE_URL=postgres://localhost:5432/your_database_cl8
```

### Set up front end toolchains

Constellate uses a toolchain based around Tailwind for generating CSS files for the front end, and MJML to make 
html emails easier to maintain. Assuming you have a recent version of nodejs installed (18+), you can run the following command

```
just install
```

### Run any migrations 

You will need to run migrations to set up your blank database

```
just manage migrate
```

### Run a local server

You can now run a local server. If you're running locally you will want to generate the css needed for your site
using tailwind 

```
just tailwind-build
```

Or if you want to generate css files continuously, open a second terminal window and run the following command:

```
@tailwind-server
```

Finally, run the django server itself:

```
just serve
```


