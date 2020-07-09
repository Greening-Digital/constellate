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

    name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)

    def add_photo_url(self, instance):
        """
        Add the photo url for the output representation of a profile object.
        """

        url = instance.photo.url
        
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)

        return url

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['photo'] = self.add_photo_url(instance)
        return res


    def create(self, validated_data, user=None):

        ModelClass = self.Meta.model

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

    def update(self, instance, validated_data):

        for user_key in ['name', 'email', 'admin']:
            if user_key in validated_data.keys():
                value = validated_data.pop(user_key)

                if user_key == 'admin':
                    instance.is_staff = value
                else:
                    setattr(instance.user, user_key, value)

        instance.user.save()

        for attr, value in validated_data.items():

            # some values we don't want to allow setting
            # via the API
            if attr in ['id', 'tags']:
                continue

            if not value:
                continue

            setattr(instance, attr, value)
        instance.save()

        return instance


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
        ]



