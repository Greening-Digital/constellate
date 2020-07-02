import pytest

from backend.users.models import User, Profile

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"

class TestProfile:
    def test_user_profile(self, profile: Profile):
        assert profile.email == profile.user.email

