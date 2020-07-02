import pytest

from backend.users.models import User, Profile
from backend.users.tests.factories import UserFactory, ProfileFactory, FakePhotoProfileFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()

@pytest.fixture
def profile(user) -> Profile:
    return ProfileFactory(user=user)

@pytest.fixture
def fake_photo_profile(user) -> Profile:
    return FakePhotoProfileFactory(user)
