import pytest
from django.test import RequestFactory

from backend.users.api.views import ProfileViewSet
from backend.users.models import User, Profile

pytestmark = pytest.mark.django_db

class TestProfileViewSet:
    def test_get_queryset(self, profile: Profile, rf: RequestFactory):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile.user

        view.request = request

        assert profile in view.get_queryset()

    @pytest.mark.only
    def test_me(self, profile: Profile, rf: RequestFactory):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile.user

        view.request = request
        response = view.me(request)

        for prop in [
            "name",
            "email",
            "website",
            "twitter",
            "facebook",
            "linkedin",
            "visible",
            "tags",
        ]:
            assert response.data[prop] == getattr(profile, prop)
