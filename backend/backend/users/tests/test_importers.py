import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import RequestFactory

from collections import OrderedDict

from pathlib import Path


from backend.users.importers import ProfileImporter, User

pytestmark = pytest.mark.django_db


@pytest.fixture
def generated_users():
    pass


@pytest.fixture
def csv_path():
    return Path(__file__).parent / "generated-sample-data.csv"


class TestImporter:

    """
    This importer accepts a CSV file, and creates a user for every row in the CSV file.


    """

    def test_load_csv(self, csv_path):
        """
        Load a CSV into memory, so we can manipulate it easily.
        """
        importer = ProfileImporter()
        importer.load_csv(csv_path)
        assert len(importer.rows) > 0
        assert len(importer.rows) < 400

    def test_create_users(self, csv_path):
        """
        Create a user with the provided email address
        """
        importer = ProfileImporter()
        importer.load_csv(csv_path)
        assert User.objects.count() == 0
        importer.create_users()

        assert User.objects.count() == len(importer.rows)

    def test_create_user(self, csv_path):

        importer = ProfileImporter()
        importer.load_csv(csv_path)

        user = importer.create_user(importer.rows[0])

        assert User.objects.first() == user

    @pytest.mark.parametrize(
        "tag_string, tag_list,col_names",
        (
            ("tag1, tag2, tag3", ["tag1", "tag2", "tag3"], ["tags"]),
            ("tag1, tag2, tag3", ["tag1", "tag2", "tag3"], []),
        ),
    )
    def test_add_tags_to_user(self, profile, tag_string, tag_list, col_names):

        # arrange
        importer = ProfileImporter()
        row = OrderedDict()
        row["tags"] = tag_string

        # act
        tagged_profile = importer.add_tags_to_profile(profile, row, col_names)

        # assert
        for tag in tag_list:
            assert tag in tagged_profile.tags.names()

    def test_add_multiple_kinds_of_tags_to_user(self, profile):

        # arrange
        first_tag_string = "tag1, tag2, tag3"
        second_tag_string = "tag4, tag5, tag6"
        importer = ProfileImporter()
        row = OrderedDict()
        row["tags"] = first_tag_string
        row["some_other_name"] = second_tag_string

        # act
        tagged_profile = importer.add_tags_to_profile(
            profile, row, ["tags", "some_other_name"]
        )

        # assert
        for tag in first_tag_string.split(","):
            assert tag.strip() in tagged_profile.tags.names()

        for tag in second_tag_string.split(","):
            assert tag.strip() in tagged_profile.tags.names()

