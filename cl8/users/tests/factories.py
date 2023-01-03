import io
from typing import Any, Sequence

import factory
import requests
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from factory import (
    Faker,
    RelatedFactory,
    SubFactory,
    post_generation,
)
from factory.django import DjangoModelFactory
from factory.django import ImageField as ImageFieldFactory
from taggit.models import Tag

from ..models import Profile

from faker import Faker as FakerLib


def generated_realistic_profile_photo():
    image_bytes = requests.get("https://www.thispersondoesnotexist.com/image").content
    return io.BytesIO(image_bytes)


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        """
        After a user is created, set a password using the django `set_password`
        password method.
        """

        if extracted:
            password = extracted
        else:
            fake = FakerLib("en-US")
            password = fake.password(
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
            self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


@factory.django.mute_signals(post_save)
class ProfileUserFactory(UserFactory):
    profile = RelatedFactory(
        "cl8.users.tests.factories.ProfileFactory", factory_related_name="user"
    )


@factory.django.mute_signals(post_save)
class FakePhotoProfileUserFactory(UserFactory):
    profile = RelatedFactory(
        "cl8.users.tests.factories.FakePhotoProfileFactory",
        factory_related_name="user",
    )


def url_factory():
    fake = FakerLib("en-US")
    return f"https://{fake.domain_name()}"


class TagFactory(DjangoModelFactory):

    name = Faker("word")

    class Meta:
        model = Tag


@factory.django.mute_signals(post_save)
class ProfileFactory(DjangoModelFactory):

    # make a profile tied to a user
    user = SubFactory(UserFactory)
    phone = Faker("phone_number")
    website = factory.LazyFunction(url_factory)
    twitter = Faker("user_name")
    facebook = Faker("user_name")
    linkedin = Faker("user_name")
    organisation = Faker("company")
    bio = Faker("paragraph")
    # tags = SubFactory(TagFactory)

    user = factory.SubFactory("cl8.users.tests.factories.UserFactory", profile=None)

    class Meta:
        model = Profile


@factory.django.mute_signals(post_save)
class FakePhotoProfileFactory(ProfileFactory):

    photo = factory.LazyAttribute(
        lambda o: ContentFile(
            ImageFieldFactory()._make_data(
                {"width": 400, "height": 400, "format": "jpeg"}
            ),
            "test_pic.jpg",
        )
    )

    class Meta:
        model = Profile
