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

    def create(self, validated_data, user=None):


        # raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # import ipdb ; ipdb.set_trace()

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        validated_data['user_id'] = user.id

        try:
            instance = ModelClass.objects.create(**validated_data)
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



