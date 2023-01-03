import pytest
from django.urls import resolve, reverse

from cl8.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"username": user.username})
        == f"/users/{user.username}/"
    )
    assert resolve(f"/users/{user.username}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/users/~update/"
    assert resolve("/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/users/~redirect/"
    assert resolve("/users/~redirect/").view_name == "users:redirect"


def test_cms():
    """Do we have the flat pages CMS active?"""
    # check one way…
    assert reverse("about") == "/about/"
    # and the other
    assert resolve("/about/").func.__name__ == "flatpage"
    assert resolve("/about/").kwargs["url"] == "/about/"
