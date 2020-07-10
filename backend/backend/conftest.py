import pytest

import factory
import random
from backend.users.models import User, Profile
from backend.users.tests.factories import UserFactory, ProfileFactory, FakePhotoProfileFactory
import shutil
from pathlib import Path


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



@pytest.fixture
def tmp_pic_path(tmp_path):
    filename = "test_pic.png"
    pic_path = Path().cwd() / 'backend' / 'users' / 'tests' / 'test_pic.png'
    test_pic_path = tmp_path / filename
    shutil.copy(pic_path, test_pic_path)
    return test_pic_path
