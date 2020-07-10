import pytest

import factory
import random
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
def profile_with_tags(user) -> Profile:
    profile = ProfileFactory(user=user)
    words = factory.Faker('words', nb=random.randint(0,6)).generate()
    profile.tags.add(*words)
    return profile

@pytest.fixture
def fake_photo_profile(user) -> Profile:
    return FakePhotoProfileFactory(user)
