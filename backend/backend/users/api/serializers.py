from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

User = get_user_model()
from ..models import Profile

class ProfileSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

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
        ]

