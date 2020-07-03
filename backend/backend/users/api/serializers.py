from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer,
    TagList,
)

User = get_user_model()
from ..models import Profile


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

    tags = ConstellateTagListSerializerField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "name",
            "email",
            "tags",
            "website",
            "twitter",
            "facebook",
            "linkedin",
            "bio",
            "visible",
            "photo",
            "admin",
        ]

