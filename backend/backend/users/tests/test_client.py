import requests
import pytest

# import logging
# console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
# logger = logging.getLogger(__file__)
# logger.addHandler(console)
# logger.setLevel(logging.DEBUG)

pytestmark = pytest.mark.django_db

class TestIntegrationTestForCRUD:


    def test_auth_with_toke(self, profile, client):

        # set password for user

        profile.user.set_password('topsecret')
        payload = {"username": profile.user.username, "password": 'topsecret'}

        response = client.post("auth-token/", payload)

        import ipdb ; ipdb.set_trace()
        data = response.json()
        token = data.get('token')

        import ipdb ; ipdb.set_trace()
        assert token

# logger.info(f"Token: {token}")

# post_data = {
#     "id": 1,
#     "name": "Chris Adams",
#     "email": "wave+local@chrisadams.me.uk",
#     "tags": [
#         "third one"
#     ],
#     "website": "http://chrisadams.me.uk",
#     "twitter": "",
#     "facebook": "",
#     "linkedin": "",
#     "bio": "This should not be required",
#     "visible": False,
# }
# headers =  {f"Authorization": f"Token {data.get('token')}"}

# new_response = requests.patch("http://localhost:8000/api/profiles/1/", json=post_data, headers=headers)

# logger.info(new_response)