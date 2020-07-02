import csv
from pathlib import Path
import requests

from backend.users.models import User, Profile
from django.core.files.images import ImageFile
# How it works

# We instantiate the CSV import, and either load the path to the file, or load the file directly.

# once we have that we iterate through each row, and create a user and the necessary tags
import logging

logger = logging.getLogger(__file__)

class ProfileImporter:

    rows = []

    # def __init__(self):

    def load_csv(self, import_path: Path = None):
        # Loads the rows contents of a CSV, returning an datastructure
        self.rows = []
        with open(import_path) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                self.rows.append(row)

    def create_users(self, rows=None):
        if not rows:
            rows = self.rows

        created_users = []

        for count, row in enumerate(rows):

            logger.info(f"{count}, {row['name']}, rows to run through: {len(rows)}")
            new_user = self.create_user(row)
            created_users.append(new_user)

        logger.info("made it")

        return created_users

    def create_user(self, row):
        """
        Accepts a row, and returns the corresponding user generated based on the info passed in
        """
        if not row['email']:
            return None

        # create django user
        user = User(
            name = row['name'],
            email = row['email'],
            username = row['name']
        )
        logger.info(user)
        # import ipdb ; ipdb.set_trace()
        user.save()
        logger.info(user.id)

        # import ipdb ; ipdb.set_trace()
        visible = row['visible'] == 'visible' or row['visible'] == 'true' or row['visible'] == 'yes'


        profile = Profile(
            user=user,
            phone=row['phone'],
            website=row['website'],
            twitter=row['twitter'],
            facebook=row['facebook'],
            linkedin=row['linkedin'],
            bio=row['blurb'],
            visible=visible,
            photo=self.fetch_user_pic(row['photo'])
        )
        # create corresponding profile
        profile.save()
        logger.info(profile)
        logger.info(profile.user)
        logger.info(profile.user.id)

        return user

    def fetch_user_pic(self, url: str = None):
        """
        """
        if not url:
            return None

        res = requests.get(url)

        if res.content:
            return ImageFile(res.content)

