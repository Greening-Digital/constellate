from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import ProfileSerializer
from ..models import Profile

User = get_user_model()

class ProfileViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = ProfileSerializer(request.user.profile, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
