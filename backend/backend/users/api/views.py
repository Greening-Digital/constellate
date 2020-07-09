from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import ProfileSerializer
from ..models import Profile
from django.utils.text import slugify

from django.urls import resolve

from django.http import HttpRequest, QueryDict

User = get_user_model()


class ProfileViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "id"


    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = ProfileSerializer(
            request.user.profile, context={"request": request}
        )
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):

        # make our request data a mutable dict, with the
        # values we need, and discard empty ones
        if isinstance(request.data, QueryDict):
            request_data = request.data.dict()
        else:
            request_data = request.data

        email = request_data.pop("email")
        full_name = request_data.pop("name")
        username = slugify(full_name)

        # validate User with User serializer
        new_user = User.objects.create_user(username, email, name=full_name)

        # create our profile
        request_data["user_id"] = new_user.id

        serialized_profile = ProfileSerializer(data=request_data)
        serialized_profile.is_valid(raise_exception=True)
        serialized_profile.create(serialized_profile.validated_data, user=new_user)

        headers = self.get_success_headers(serialized_profile.data)
        return Response(
            serialized_profile.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop("partial", False)

        if isinstance(request.data, QueryDict):
            request_data = request.data.dict()
        else:
            request_data = request.data

        profile_id = resolve(request.path).kwargs['id']
        instance = Profile.objects.get(id=profile_id)

        serialized_profile = self.serializer_class(
            instance, data=request_data, partial=partial
        )
        serialized_profile.is_valid(raise_exception=True)
        serialized_profile.update(instance, serialized_profile.validated_data)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serialized_profile.data)

