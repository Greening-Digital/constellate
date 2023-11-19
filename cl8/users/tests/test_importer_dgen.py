import json
import pathlib
from collections import OrderedDict

import pytest
import rich

from cl8.users.importers import FireBaseImporter


pytestmark = pytest.mark.django_db


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


class TestDGenImporter:
    def test_create_profile_from_dgen(self, dgen_data):
        profs = [prof for prof in dgen_data["userlist"].values()]

        importer = FireBaseImporter()

        for prof in profs:
            created_user = importer.create_user(prof)

            assert created_user.email == prof["fields"]["email"]
            assert created_user.name == prof["fields"]["name"]

            assert created_user.profile.visible is False
            assert created_user.profile.website == prof["fields"].get("website")
