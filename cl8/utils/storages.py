from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage
from django.conf import settings


class StaticRootS3Boto3Storage(S3StaticStorage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    """
    A subclass to default to making files public-read,
    and removing the querystring auth.
    """

    location = "media"
    default_acl = "public-read"
    # setting this to false means that you don't
    # have the long querystring on the end of the url
    # this only works for public-read files though
    querystring_auth = False
