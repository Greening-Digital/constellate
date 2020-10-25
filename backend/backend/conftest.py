import pytest

import factory
import random
from backend.users.models import User, Profile
from backend.users.tests.factories import (
    UserFactory,
    ProfileFactory,
    FakePhotoProfileFactory,
)
import shutil
from pathlib import Path
from django.contrib.auth.models import Group, Permission
from django.conf import settings


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
    words = factory.Faker("words", nb=random.randint(0, 6)).generate()
    profile.tags.add(*words)
    return profile


@pytest.fixture
def fake_photo_profile(user) -> Profile:
    return FakePhotoProfileFactory(user=user)


@pytest.fixture
def tmp_pic_path(tmp_path):
    filename = "test_pic.png"
    pic_path = Path().cwd() / "backend" / "users" / "tests" / "test_pic.png"
    test_pic_path = tmp_path / filename
    shutil.copy(pic_path, test_pic_path)
    return test_pic_path


@pytest.fixture
def moderator_group():
    # the moderator group
    grp = Group(name=settings.MODERATOR_GROUP_NAME)
    grp.save()
    desired_perms = [
        "Can add tag",
        "Can change tag",
        "Can delete tag",
        "Can view tag",
        "Can add Cluster",
        "Can change Cluster",
        "Can delete Cluster",
        "Can view Cluster",
        "Can add Profile",
        "Can change Profile",
        "Can delete Profile",
        "Can view Profile",
        "Can add user",
        "Can change user",
        "Can delete user",
        "Can view user",
    ]
    for perm in desired_perms:
        perm_records = Permission.objects.filter(name__in=desired_perms)
        grp.permissions.set(perm_records)

    return grp
