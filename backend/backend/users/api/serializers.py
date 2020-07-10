from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer,
    TagList,
)

from rest_framework.utils import model_meta

User = get_user_model()
from ..models import Profile
from django.utils.text import slugify


class ConstellateTagListSerializerField(TagListSerializerField):
    """
    We need to override the tag serialise to create the datastructure
    that the client expects.
    """

    def to_representation(self, value):
        if not isinstance(value, TagList):
            if not isinstance(value, list):
                if self.order_by:
                    tags = value.all().order_by(*self.order_by)
                else:
                    tags = value.all()

                value = [
                    {"id": tag.id, "slug": tag.slug, "name": tag.name} for tag in tags
                ]
            value = TagList(value, pretty_print=self.pretty_print)

        return value

class ProfileSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = ConstellateTagListSerializerField(required=False)

    name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    admin = serializers.BooleanField(required=False)

    def create(self, validated_data, user=None):

        ModelClass = self.Meta.model

        email = validated_data.pop("email")
        full_name = validated_data.pop("name")
        admin = validated_data.pop("admin", False)
        username = slugify(full_name)

        # create our related User from the details passed in
        new_user = User(
            username=username,
            email=email,
            name=full_name,
            is_staff=admin,
        )

        # if you don't set password like this this, you get an
        # unhashed string, as django makes no assumptions about
        # the hashing algo to use
        new_user.set_password(None)
        new_user.save()

        try:

            to_be_tagged, validated_data = self._pop_tags(validated_data)

            instance = ModelClass.objects.create(**validated_data, user=new_user)

            # then save our updated tags too
            self.update_tags(instance, to_be_tagged)

        except TypeError as exc:
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception text was: %s.' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    exc
                )
            )
            raise TypeError(msg)

        return instance

    def update(self, instance, validated_data):

        # update our corresponding user first
        instance.user.name = validated_data.pop('name', instance.user.name)
        instance.user.email = validated_data.pop('email', instance.user.email)
        instance.user.is_staff = validated_data.pop('admin', False)
        instance.user.save()

        # we need to update the tags separately to the other properties
        validated_data = self.update_tags(instance, validated_data)

        # finally update the profile itself
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def update_tags(self, instance, validated_data):

        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tag_object = super(TaggitSerializer, self).update(
            instance, validated_data)

        saved_tags = self._save_tags(tag_object, to_be_tagged)

        return validated_data




    class Meta:
        model = Profile
        fields = [
            "id",

            # user
            "name",
            "email",

            # profile
            "phone",
            "website",
            "twitter",
            "facebook",
            "linkedin",
            "bio",

            "visible",
            "admin",

            # need their own handler
            "tags",
            "photo",
        ]
        read_only_fields = ["photo", "id"]


class ProfilePicSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    photo =  serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('id', 'photo')