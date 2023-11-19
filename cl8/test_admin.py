import json
from logging import getLogger

import pytest
from django.core.files.base import ContentFile

from .admin import FirebaseImportForm, CsvImportForm
from .users.models import Profile, User

import pathlib

logger = getLogger(__name__)


@pytest.fixture
def sample_csv_path():
    """Return the path to a sample csv file"""
    return (
        pathlib.Path(__file__).parent / "users" / "tests" / "generated-sample-data.csv"
    )


@pytest.fixture
def dgen_data():
    return {
        "userlist": {
            "-L5zIhS_QRqoblu55nGI": {
                "fields": {
                    "admin": "false",
                    "email": "name@domain.com",
                    "name": "A name of multiple words",
                    "tags": [
                        {"id": "rec7BPWAthDqPSOeY", "name": "policy"},
                        {"id": "recoHNloW0Nk9M9JK", "name": "Leadership"},
                        {"id": "recvyDsYcNdJx91is", "name": "tech"},
                    ],
                    "visible": "no",
                    "website": "just-a-naked-domain.com",
                },
                "id": "rec0CSbkZBm1wWluF",
            }
        }
    }


pytestmark = pytest.mark.django_db


class TestFirebaseProfileImportForm:
    # csv_text_file = StringIO(csv_file.read().decode("utf-8"))

    def test_firebase_import_via_form_checks_validity(self, dgen_data):
        json_file = ContentFile(json.dumps(dgen_data).encode(), name="test_import.json")

        test_data = {
            "import_photos": False,
        }
        uploaded_files = {
            "firebase_json": json_file,
        }

        # forms are multipart, so we need to pass in the files separately
        form = FirebaseImportForm(test_data, uploaded_files)

        form.is_valid()

        logger.debug(form.errors)
        logger.debug(form.cleaned_data)

        assert form.is_valid()

    def test_firebase_import_via_form_creates_profiles(self, dgen_data):
        json_file = ContentFile(json.dumps(dgen_data).encode(), name="test_import.json")

        test_data = {
            "import_photos": False,
        }
        uploaded_files = {
            "firebase_json": json_file,
        }

        # forms are multipart, so we need to pass in the files separately
        form = FirebaseImportForm(test_data, uploaded_files)

        form.is_valid()
        form.save()

        profile = Profile.objects.first()

        assert Profile.objects.count() == 1
        assert User.objects.count() == 1

        assert profile.user == User.objects.first()

        # now check sample data
        profile_data = dgen_data["userlist"]["-L5zIhS_QRqoblu55nGI"]

        assert profile.user.email == profile_data["fields"]["email"]
        assert profile.name == profile_data["fields"]["name"]


class TestCSVProfileImportForm:
    def test_csv_import_via_form_checks_validity(self, sample_csv_path):
        logger.info(sample_csv_path)

        text = sample_csv_path.read_text()

        import_file = ContentFile(
            sample_csv_path.read_text(), name=sample_csv_path.name
        )

        test_data = {}
        uploaded_files = {
            "import_file": import_file,
        }

        # forms are multipart, so we need to pass in the files separately
        form = CsvImportForm(test_data, uploaded_files)

        assert form.is_valid()

        logger.debug(form.errors)
        logger.debug(form.cleaned_data)

    def test_csv_import_via_form_creates_profiles(self, sample_csv_path):
        logger.info(sample_csv_path)

        # we encode our file to bytes because this matches what is sent by the browser
        import_file = ContentFile(
            sample_csv_path.read_text().encode(), name=sample_csv_path.name
        )

        test_data = {}
        uploaded_files = {
            "import_file": import_file,
        }

        # forms are multipart, so we need to pass in the files separately
        form = CsvImportForm(test_data, uploaded_files)

        assert form.is_valid()
        form.save()

        # we have 7 profile rows in our sample csv
        assert Profile.objects.count() == 7
        assert User.objects.count() == 7

        profile = Profile.objects.first()
        assert profile.user == User.objects.get(email=profile.email)
