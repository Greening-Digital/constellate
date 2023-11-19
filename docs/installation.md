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

### Working with files stored in object storage 

Constellate is set up to work with S3-compatible object storage, and in production, the application is assumed to be stateless and disposable, with the important state stored in object storage or the database.

** Working in development **

To make working with files in development easier the AWS CLI is installed in the development dependencies. However to make this work with S3 compatible providers like Scaleway, Digital Ocean, Cloudflare and so on, you need to add two files to the project directory then set two environment variables.

**An aws.config file** 

This is needed by the `awscli_plugin_endpoint` python package that makes the aws-cli project work with multiple providers.

Set up for scaleway, the content looks like so:

```
[plugins]
endpoint = awscli_plugin_endpoint

[default]
# for scaleway can be nl-ams (Amsterdam), fr-par (Paris), or pl-waw (Warsaw)
region = nl-ams
s3 =
  endpoint_url = https://s3.nl-ams.scw.cloud
  signature_version = s3v4
  max_concurrent_requests = 100
  max_queue_size = 1000
  multipart_threshold = 50MB
  # Edit the multipart_chunksize value according to the file sizes that you want to upload.
  # The present configuration allows to upload files up to 10 GB (1000 requests * 10MB).
  # For example setting it to 5GB allows you to upload files up to 5TB.
  multipart_chunksize = 10MB
s3api =
  endpoint_url = https://s3.nl-ams.scw.cloud

```

You can copy the `aws.config.sample` file in this repo to get a head start.

Once this is set up, you set the `AWS_CONFIG_FILE` environment variable to point to the absolute path for this file on your server. Setting this with a `.env` file is convenient for development.

**An aws.credentials file** 

You then need to do the same for a credentials file, so requests to the object storage service use the correct credentials. Copy the `aws.credentials.sample` file, and add your own credentials from your provider. It should look like so:

```
[default]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Set the `AWS_SHARED_CREDENTIALS_FILE` environment variable to point to the absolute path for this file on your server too. 


Once you have these you should be able to run common AWS S3 commands against your preferred provider:


```shell

# see the buckets available to you
aws s3 ls
# 2023-11-01 09:39:26 my-bucket

aws s3 ls my-bucket
#           PRE media/

# see what you have uploaded already
aws s3 ls my-bucket/
#           PRE cache/
#           PRE logos/
#           PRE photos/

# copy one file
aws s3 cp s3://my-bucket/photos/some-pic ./media/photos/some-pic

# copy all the files matching a key to a local media server
aws s3 sync s3://my-bucket/photos/ ./media
```

Note - you still need to aws similar credentials in your `.env` file if you want your application to be able to connect to the object storage service.

Make sure the following files are set, for django storages to be able to upload files to object storage and to access them in your app:

```
DJANGO_AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXX
DJANGO_AWS_SECRET_ACCESS_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
DJANGO_AWS_STORAGE_BUCKET_NAME=my-bucket
DJANGO_AWS_S3_REGION_NAME=nl-ams
DJANGO_AWS_S3_ENDPOINT_URL=https://s3.nl-ams.scw.cloud
```

