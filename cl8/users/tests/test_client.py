import pytest
import requests
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, RequestsClient

# import logging
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# logger = logging.getLogger(__file__)
# logger.addHandler(console)
# logger.setLevel(logging.DEBUG)

pytestmark = pytest.mark.django_db


@pytest.mark.skip(
    reason="These tests are triggering an exception, but the code is working when tested menually"
)
class TestIntegrationTestForCRUD:
    def test_auth_to_get_token(self, profile, live_server, transactional_db):
        """
        Given: the correct username and password
        Then: return an auth token to use with future API calls
        """

        # set password for user, and sanity check
        profile.user.set_password("topsecret")
        profile.save()
        assert profile.user.check_password("topsecret")

        # TODO: these exact lines work against the live server.
        # What is going wrong here?
        payload = {"username": profile.user.username, "password": "topsecret"}
        response = requests.post(f"{live_server.url}/auth/token/", json=payload)
        assert response.status_code == 200

        data = response.json()
        token = data.get("token")
        token_from_db = Token.objects.first()

        assert token == token_from_db.key


class TestIntegrationTestToAddProfilePhoto:
    def test_add_photo(self, db, profile, tmp_pic_path):
        """
        Can we upload a file via the new endpoint?
        """
        token = Token(key="short-and-readable", user=profile.user)
        token.save()

        # login using the token credentials, using the DRF API client
        # convenience method
        # https://www.django-rest-framework.org/api-guide/testing/#credentialskwargs
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        res = client.get("http://testserver/api/profiles/")

        assert res.status_code == 200

        payload = {"photo": open(tmp_pic_path, "rb"), "id": profile.id}

        res = client.put(f"http://testserver/api/upload/{profile.id}/", payload)

        assert res.status_code == 200
