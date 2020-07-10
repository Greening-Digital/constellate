from typing import Any, Sequence
import io
from django.contrib.auth import get_user_model
from ..models import Profile
import factory
from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    SubFactory,
    RelatedFactory,
    SelfAttribute,
)
from factory.django import ImageField as ImageFieldFactory
import requests
from django.db.models.signals import post_save

from taggit.models import Tag

def generated_profile_photo():
    image_bytes = requests.get("https://www.thispersondoesnotexist.com/image").content
    return io.BytesIO(image_bytes)


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


@factory.django.mute_signals(post_save)
class ProfileUserFactory(UserFactory):
    profile = RelatedFactory(
        "backend.users.tests.factories.ProfileFactory", factory_related_name="user"
    )


@factory.django.mute_signals(post_save)
class FakePhotoProfileUserFactory(UserFactory):
    profile = RelatedFactory(
        "backend.users.tests.factories.FakePhotoProfileFactory", factory_related_name="user"
    )

def url_factory():
    domain_generator = factory.Faker('domain_name')
    return f"https://{domain_generator.generate()}"


class TagFactory(DjangoModelFactory):

    name = Faker('word')

    class Meta:
        model = Tag




def list_of_tags():
    website = factory.LazyFunction(url_factory)


@factory.django.mute_signals(post_save)
class ProfileFactory(DjangoModelFactory):



    # make a profile tied to a user
    user = SubFactory(UserFactory)
    phone = Faker("phone_number")
    website = factory.LazyFunction(url_factory)
    twitter = Faker("user_name")
    facebook = Faker("user_name")
    linkedin = Faker("user_name")
    bio = Faker("paragraph")

    # tags = SubFactory(TagFactory)

    user = factory.SubFactory("backend.users.tests.factories.UserFactory", profile=None)

    class Meta:
        model = Profile

@factory.django.mute_signals(post_save)
class FakePhotoProfileFactory(ProfileFactory):

    photo = ImageFieldFactory(from_func=generated_profile_photo)

    class Meta:
        model = Profile
