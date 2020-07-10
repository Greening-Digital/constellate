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


from django.urls import resolve

from django.http import HttpRequest, QueryDict
from rest_framework.utils.serializer_helpers import ReturnDict

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

        serialized_profile = ProfileSerializer(request.user.profile)
        return Response(status=status.HTTP_200_OK, data=serialized_profile.data)

    def create(self, request):

        serialized_profile = ProfileSerializer(data=request.data)
        serialized_profile.is_valid(raise_exception=True)
        new_profile = serialized_profile.create(serialized_profile.data)

        full_serialized_profile = ProfileSerializer(new_profile)

        headers = self.get_success_headers(full_serialized_profile.data)
        return Response(
            full_serialized_profile.data, status=status.HTTP_201_CREATED, headers=headers
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

