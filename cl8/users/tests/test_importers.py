import json
import pathlib
from collections import OrderedDict

import pytest
import rich

from cl8.users.importers import CSVImporter, User

from .. import importers

pytestmark = pytest.mark.django_db


@pytest.fixture
def generated_users():
    pass


@pytest.fixture
def csv_path():
    return pathlib.Path(__file__).parent / "generated-sample-data.csv"


class TestImporter:

    """
    This importer accepts a CSV file, and creates a user for every row in the CSV file.


    """

    def test_load_csv(self, csv_path):
        """
        Load a CSV into memory, so we can manipulate it easily.
        """
        importer = CSVImporter()
        importer.load_csv_from_path(csv_path)
        assert len(importer.rows) > 0
        assert len(importer.rows) < 400

    def test_create_users(self, csv_path):
        """
        Create a user with the provided email address
        """
        importer = CSVImporter()
        importer.load_csv_from_path(csv_path)
        assert User.objects.count() == 0
        importer.create_users()

        assert User.objects.count() == len(importer.rows)

    def test_create_user(self, csv_path):
        importer = CSVImporter()
        importer.load_csv_from_path(csv_path)

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
        importer = CSVImporter()
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
        importer = CSVImporter()
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


@pytest.fixture
def join_request_row():
    return [
        "7/15/2019 16:02:11",
        "some.person@gmail.com",
        "Sure, sign me up",
        "",
        "I'm building a social reforestation app",
        "I can offer feedback, suggestions, tips at the moment. I'm an engineer.",
        "Yes I have read the code of conduct, and agree to follow it.",
        "",
    ]


@pytest.fixture
def join_requests_data():
    json_path = pathlib.Path().cwd() / "data" / "local.responses.json"

    parsed_data = json.loads(json_path.read_text())
    return parsed_data[1:]


@pytest.mark.skip(
    reason="Was only used to sanity check the importer against a local data snapshot"
)
def test_create_join_request(join_request_row):
    res = importers.create_join_request_from_row(join_request_row)

    assert res.id


@pytest.mark.skip(reason="Waiting for new dummy test data to be created")
def test_create_join_request_for_all(join_requests_data):
    created = []
    errors = []

    for row in join_requests_data:
        try:
            res = importers.create_join_request_from_row(row)
            created.append(res)
        except importers.NoMatchingCAT as ex:
            errors.append(ex)
        except importers.EmptyJoinRequestCAT as ex:
            errors.append(ex)

    rich.print(
        f"total_imported: {len(created)} from a possible {len(join_requests_data)}"
    )
    rich.print(len(errors))
    assert len(created) > 8
