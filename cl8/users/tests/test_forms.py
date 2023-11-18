import pytest

from cl8.users.forms import UserCreationForm
from cl8.users.forms import ProfileCreateForm
from cl8.users.tests.factories import UserFactory
from taggit.models import Tag

pytestmark = pytest.mark.django_db


class TestUserCreationForm:
    def test_clean_username(self):
        """
        Given: an existing user with a given username
        Then: submissions to creating a user with the same name
        should not be valid
        """
        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()

        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )
        assert form.is_valid()
        assert form.clean_username() == proto_user.username

        # Creating a user.
        form.save()

        # The user with proto_user params already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors


class TestProfileCreationForm:
    def test_create_profile(self):
        """
        Given: a user
        When: a profile is created
        Then: the profile is created along with the user it depends on
        """

        test_tag = Tag.objects.create(name="test")

        test_data = {
            "name": "Test User",
            "email": "person@local.host",
            "tags": [test_tag.id],
        }

        form = ProfileCreateForm(test_data)
        assert form.is_valid()
        form.save()

        assert form.instance.name == test_data.get("name")
        assert form.instance.user.email == "person@local.host"
