import csv
import io
import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import List

import requests
import slack
from django.conf import settings
from django.core.files.images import ImageFile
from django.utils.text import slugify

from .models import Profile, User

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


class NoEmailFound(Exception):
    pass


def safe_username(username):
    """
    Adjust a username to avoid naming collisions.
    """
    safer_int = str(datetime.now().microsecond)[:4]
    return f"{slugify(username)}-{safer_int}"


class ProfileImporter:

    rows = []

    def load_csv_from_path(self, import_path: Path = None):
        with open(import_path) as csvfile:
            self.load_csv(csvfile)

    def load_csv(self, csvfile=None):
        # Loads the rows contents of a CSV, returning a datastructure
        self.rows = []

        reader = csv.DictReader(csvfile)

        for row in reader:
            self.rows.append(row)

    def create_users(self, rows=None):
        if not rows:
            rows = self.rows

        created_users = []
        skipped_users = []

        for count, row in enumerate(rows):

            logger.debug(f"Importing. Rows to run through: {len(rows)}")
            try:
                new_user = self.create_user(row)
                created_users.append(new_user)
            except NoEmailFound:
                skipped_users.append(row)

        logger.debug(f"Added {len(created_users)}")
        logger.debug(f"Skipped {len(created_users)}")

        return created_users

    def add_tags_to_profile(
        self, profile: Profile, row: OrderedDict, columns: List = None
    ):
        """
        Take a profile object, and add all the relevant tags,
        in the properties from the CSV listed `columns`.
        """
        if not columns:
            columns = ["tags"]

        for colname in columns:
            tags = row.get(colname)
            # exit early
            if not tags:
                continue

            for tag in tags.split(","):
                profile.tags.add(tag.strip())

        return profile

    def create_user(self, row):
        """
        Accepts a row, and returns the corresponding user generated based
        on the info passed in
        """

        if not row["email"]:
            raise (NoEmailFound)

        # create django user
        safer_int = str(datetime.now().microsecond)[:4]
        safer_name = f"{slugify(row['name'])}-{safer_int}"

        user, created = User.objects.get_or_create(email=row["email"])

        logger.debug(user)
        user.name = row["name"]
        user.username = safer_name
        user.save()
        logger.debug(user.id)

        visible = True

        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = row.get("phone")
        profile.website = row.get("website")
        profile.twitter = row.get("twitter")
        profile.facebook = row.get("facebook")
        profile.linkedin = row.get("linkedin")
        profile.bio = row.get("bio")
        profile.visible = visible
        profile.photo = self.fetch_user_pic(row.get("photo"))
        self.add_tags_to_profile(profile, row)
        profile.save()

        logger.debug(f"profile: {profile}")
        logger.debug(f"user: {user}")
        logger.debug(profile.user.id)

        profile.save()
        return user

    def fetch_user_pic(self, url: str = None):
        """
        """
        if not url:
            return None

        res = requests.get(url)

        if res.content:
            return ImageFile(res.content)


class SlackImporter:
    """
    An importer for fetching a list of users from a given channel in
    a slack workspace, then adding each user to a given constellation.
    """

    def __init__(self):
        self.client = slack.WebClient(token=settings.SLACK_TOKEN)

    def _fetch_user_ids(self):
        """Fetch a list of users from slack"""

        channel_id = self._id_for_channel_name(settings.SLACK_CHANNEL_NAME)
        user_ids = []

        response = self.client.conversations_members(channel=channel_id).data
        cursor = response["response_metadata"].get("next_cursor")
        user_ids = [*response["members"]]

        # we paginate through the responses because some channels have more
        # than 100 members in them
        while cursor:
            logger.info(f"paginating with cursor: {cursor}")
            resp = self.client.conversations_members(channel=channel_id, cursor=cursor)
            user_ids = [*user_ids, *resp["members"]]
            cursor = resp["response_metadata"].get("next_cursor")

        return user_ids

    def _id_for_channel_name(self, channel_name):
        """
        Accept a channel name, and return the channel id for further use
        with slack API
        """

        response = self.client.conversations_list(types="public_channel")
        channel_name_id_pair, *rest = [
            (channel["name"], channel["id"])
            for channel in response.data["channels"]
            if channel["name"] == channel_name
        ]
        if channel_name_id_pair:
            chan_name, chan_id = channel_name_id_pair
            logger.debug(f"Found channel id {chan_id} for channel #{chan_name}")
            return chan_id

    def _fetch_user_for_id(self, user_id):
        """
        Fetch the user from the slack API with the provided user_id
        """
        return self.client.users_info(user=user_id).data["user"]

    def list_new_users(self):
        """
        Return a list of user ids for users that
        do not already exist in the constellation
        """

        import_ids = Profile.objects.all().values_list("import_id", flat=True)

        user_ids = self._fetch_user_ids()

        # we adjust the returned ids to match the format
        # kept in the local database
        adjusted_user_ids = [f"slack-{user_id}" for user_id in user_ids]

        # filter our list of new user ids from the API against the list of
        # import_ids in our local database
        return [user_id for user_id in adjusted_user_ids if user_id not in import_ids]

    def import_slack_user(self, user_id):
        """
        Accept a user id, fetch the matching user
        from slack, and import it into the constellation
        """

        # fetch the user object from slack, and extract
        # the values we want to save
        user_from_api = self._fetch_user_for_id(user_id)

        email = user_from_api["profile"]["email"]
        username = safe_username(email)
        real_name = user_from_api["profile"]["real_name_normalized"]
        photo_url = user_from_api["profile"].get("image_original")
        import_id = f"slack-{user_from_api['id']}"
        visible = True

        # add the user to constellate
        user, user_created = User.objects.get_or_create(email=email)
        user.name = real_name
        if user_created:
            user.username = username
        user.save()

        # add the matching profile to constellate for user
        profile, profile_created = Profile.objects.get_or_create(user=user)

        # then add the info we have from the API
        profile.import_id = import_id
        if photo_url:
            profile.photo = self.fetch_user_pic(photo_url)

        # default to being visible for directory
        profile.visible = visible
        profile.save()
        user.save()

        return user

    def import_users(self):
        """
        Fetch users from slack for a channel,
        and import all the new users.
        """

        new_ids = self.list_new_users()

        imported_users = []
        for new_user_id in new_ids:
            imported_user = self.import_slack_user(new_user_id)
            imported_users.append(imported_user)

        return imported_users

    def fetch_user_pic(self, url: str = None):
        """
        """
        if not url:
            return None
        try:
            res = requests.get(url)
        except Exception as err:
            logger.warning(f"Unable to get url: {url}: Error: {err}")

        if res.content:
            filename = url.split("/")[-1]
            return ImageFile(io.BytesIO(res.content), name=filename)


class CATAirtableImporter(ProfileImporter):
    """
    An importer to take the current data stored in an airtable, and update a user's info
    with the data in the provided CSV file - uses email address as the key to match on.
    """

    def create_user(self, row):
        """
        Accepts a row, and returns the corresponding user generated based
        on the info passed in
        """
        email_key = "Email address"
        email = row[email_key]
        if not email:
            raise (NoEmailFound)

        logger.info(f"email: {email}")
        user, created = User.objects.get_or_create(email=email)
        logger.info(f"user: {user}")
        if created or not user.username:
            user.username = safe_username(row.get("email"))

        logger.info(f"user: {user}")
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)

        profile.twitter = row.get("Twitter")
        profile.linkedin = row.get("LinkedIn URL")
        profile.bio = row.get("bio")
        profile.visible = True

        self.add_tags_to_profile(profile, row)
        profile.save()
        return user

    def add_tags_to_profile(
        self, profile: Profile, row: OrderedDict, columns: List = None
    ):
        """
        Take a profile object, and add all the relevant tags,
        in the properties from the CSV listed `columns`.
        """

        # allow for override of defaults
        if not columns:
            columns = [
                "Offers",
                "Asks",
                "Specific skills",
                "Areas of focus",
            ]

        for colname in columns:
            tags = row.get(colname)
            # exit early
            if not tags:
                continue

            for tag in tags.split(","):
                profile.tags.add(f"{colname}:{tag.strip()}")

        return profile
