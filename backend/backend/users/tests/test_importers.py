import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import RequestFactory

from backend.users.models import User
from backend.users.tests.factories import UserFactory
from backend.users.importers import ProfileImporter

from pathlib import Path
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
