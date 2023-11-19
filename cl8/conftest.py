import random
import shutil
from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.contrib.sites.models import Site
from pytest_factoryboy import register

from cl8.users.models import Constellation, Profile, User
from cl8.users.tests.factories import (
    FakePhotoProfileFactory,
    ProfileFactory,
    UserFactory,
)

register(UserFactory)
register(FakePhotoProfileFactory)


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
def profile_with_tags(user, faker) -> Profile:
    profile = ProfileFactory(user=user)
    words = faker.words(nb=random.randint(0, 6))
    profile.tags.add(*words)
    return profile


@pytest.fixture
def fake_photo_profile(user) -> Profile:
    return FakePhotoProfileFactory(user=user)


@pytest.fixture
def tmp_pic_path(tmp_path):
    filename = "test_pic.png"
    pic_path = Path(__file__).parent / "users" / "tests" / "test_pic.png"
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


@pytest.fixture
def test_constellation():
    """
    Simulates the creation of a site, and a linked
    constellation
    """
    current_site = Site.objects.get_current()
    return Constellation.create(site=current_site)
