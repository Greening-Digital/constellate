from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework import serializers

from taggit.models import Tag
from taggit_serializer.serializers import (
    TaggitSerializer,
    TagList,
    TagListSerializerField,
)

User = get_user_model()


from ..models import Cluster, Profile


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
    clusters = ConstellateTagListSerializerField(required=False)

    name = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    admin = serializers.BooleanField(required=False)

    # we override these to return just the url, not do the expensive
    # back and forth communication with object storage
    # photo = serializers.CharField(source="_photo_url", read_only=True)
    thumbnail_photo = serializers.CharField(
        source="_photo_thumbnail_url", read_only=True
    )
    detail_photo = serializers.CharField(source="_photo_detail_url", read_only=True)

    def create(self, validated_data, user=None):

        ModelClass = self.Meta.model

        email = validated_data.pop("email")
        full_name = validated_data.pop("name")
        admin = validated_data.pop("admin", False)
        username = slugify(full_name)

        # create our related User from the details passed in
        new_user = User(username=username, email=email, name=full_name, is_staff=admin,)

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
                "Got a `TypeError` when calling `%s.objects.create()`. "
                "This may be because you have a writable field on the "
                "serializer class that is not a valid argument to "
                "`%s.objects.create()`. You may need to make the field "
                "read-only, or override the %s.create() method to handle "
                "this correctly.\nOriginal exception text was: %s."
                % (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    exc,
                )
            )
            raise TypeError(msg)

        return instance

    def update(self, instance, validated_data):

        # update our corresponding user first
        instance.user.name = validated_data.pop("name", instance.user.name)
        instance.user.email = validated_data.pop("email", instance.user.email)
        instance.user.is_staff = validated_data.pop("admin", False)
        instance.user.save()

        # we need to update the tags separately to the other properties
        if validated_data.get("tags"):
            validated_data = self.update_tags(instance, validated_data)

        # finally update the profile itself
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def update_tags(self, instance, validated_data):
        """
        Update tags, accounting for the different format
        sent by the Vue client.
        """

        to_be_tagged, validated_data = self._pop_tags(validated_data)
        tagged_object = super(TaggitSerializer, self).update(instance, validated_data)

        # make a dict comprehension, turning
        # ['tag1', 'tag2']
        # into
        # {'tag1': 'tag1', 'tag2': 'tag2'}
        adjusted_tags = {val: val for (key, val) in enumerate(to_be_tagged["tags"])}

        self._save_tags(tagged_object, {"tags": adjusted_tags})

        return validated_data

    def _save_tags(self, tag_object, tags):
        """
        Override of the tag serialiser, to account for tag
        info being sent in a different format via the vue client.
        """
        for key in tags.keys():
            tag_values = tags.get(key)
            # we need to wrap the tag values in a list, otherwise
            # 'tech' is turned into four tags, 't','e','c','h'
            getattr(tag_object, key).set([*tag_values])

        return tag_object

    # TODO: figure out how to represennt these fields
    # presumably, we would extend the photo serialiser field
    # def to_representation(self, instance):
    #     """
    #     Override the default representation to serve the
    #     image urls.
    #     """

    #     ret = super().to_representation(instance)

    #     # sub in the photo urls:

    #     ret["thumbnail_photo"] = instance.thumbnail_photo
    #     ret["detail_photo"] = instance.detail_photo

    #     return ret

    class Meta:
        model = Profile
        fields = [
            "id",
            # user
            "name",
            "email",
            "organisation",
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
            "clusters",
            # "photo",
            "thumbnail_photo",
            "detail_photo",
        ]
        read_only_fields = ["id", "thumbnail_photo", "detail_photo"]


class TagSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "slug",
        ]
        read_only_fields = ["id", "name", "slug"]


class ClusterSerializer(TaggitSerializer, serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = [
            "id",
            "name",
            "slug",
        ]
        read_only_fields = ["id", "name", "slug"]


class ProfilePicSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ("id", "photo")
