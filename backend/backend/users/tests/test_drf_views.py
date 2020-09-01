import pytest
from django.test import RequestFactory
from rest_framework.test import RequestsClient, APIClient
from rest_framework.authtoken.models import Token

from backend.users.api.views import ProfileViewSet, ProfilePhotoUploadView
from backend.users.models import User, Profile
from backend.users.api.serializers import ProfileSerializer
from backend.users.tests.factories import ProfileFactory
from backend.users.tests.factories import UserFactory, ProfileFactory
import shutil

from pathlib import Path

pytestmark = pytest.mark.django_db


class TestProfileViewSet:
    def test_get_queryset(self, profile: Profile, rf: RequestFactory):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile.user
        view.request = request

        assert profile in view.get_queryset()


    def test_me(self, profile_with_tags: Profile, rf: RequestFactory):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile_with_tags.user

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
        ]:
            assert response.data[prop] == getattr(profile_with_tags, prop)

        # we need to check separately for tags, as they use
        # their own manager
        response.data['tags'] = [tag for tag in profile_with_tags.tags.all()]


    def test_tag_serialised_data_structure(self, profile: Profile, rf: RequestFactory):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile.user

        # set our tags
        profile.tags.add('first tag', "second tag", "third tag")
        profile.save()

        view.request = request
        response = view.me(request)
        tags = response.data['tags']

        # are they following the structure we expect?
        for tag in tags:
            for k in ['id', 'name', 'slug']:
                assert k in tag.keys()


    def test_create_profile(self, profile: Profile, rf: RequestFactory, mailoutbox):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile.user

        profile_data = ProfileFactory()
        profile_dict = {
            'phone': '9329275526',
            'website': 'http://livingston.biz',
            'twitter': 'paul58',
            'facebook': 'fday',
            'linkedin': 'wpalmer',

            'name': 'Long Name with lots of letters',
            'email': 'email@somesite.com',
            'tags': ["tech, 'something else'', "],

            'bio': 'Themselves TV western under. Tv can beautiful we throughout politics treat both. Fear speech left get answer over century.',

            'visible': False,
        }

        request.data = profile_dict

        response = view.create(request)
        assert response.status_code == 201
        assert len(mailoutbox) == 0


    def test_create_profile_and_notify(self, profile: Profile, rf: RequestFactory, mailoutbox):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile.user

        profile_data = ProfileFactory()
        profile_dict = {
            'phone': '9329275526',
            'website': 'http://livingston.biz',
            'twitter': 'paul58',
            'facebook': 'fday',
            'linkedin': 'wpalmer',

            'name': 'Long Name with lots of letters',
            'email': 'email@somesite.com',
            'tags': ["tech, 'something else'', "],

            'bio': 'Themselves TV western under. Tv can beautiful we throughout politics treat both. Fear speech left get answer over century.',

            'visible': False,
            'sendInvite': True,
        }

        request.data = profile_dict
        response = view.create(request)

        assert response.status_code == 201
        assert len(mailoutbox) == 1

    def test_update_profile(self, profile: Profile, rf: RequestFactory):
        view = ProfileViewSet()
        request = rf.get(f"/api/profiles/{profile.id}/")
        request.user = profile.user

        profile_data = ProfileFactory()
        profile_dict = {
            'phone': '9329275526',
            'website': 'http://livingston.biz',
            'twitter': 'paul58',
            'facebook': 'fday',
            'linkedin': 'wpalmer',

            'name': 'Long Name with lots of letters',
            'email': 'email@somesite.com',
            'tags': ["tech"],

            'bio': 'Themselves TV western under. Tv can beautiful we throughout politics treat both. Fear speech left get answer over century.',

            'visible': False,
        }

        request.data = profile_dict

        response = view.update(request, profile)
        assert response.status_code == 200


@pytest.mark.skip
class TestProfileUploadView:

    def test_file_upload_for_profile(self, profile, rf, tmp_path, tmp_pic_path):
        view = ProfilePhotoUploadView()
        request = rf.get("/upload/")
        request.user = profile.user
        view.request = request

        assert not profile.photo

        filename = "test_pic.png"
        test_pic = open(tmp_pic_path, 'rb')

        request.data = {
            'photo': test_pic,
            "id": profile.id,
        }

        response = view.put(request, profile.id)
        updated_profile = Profile.objects.get(pk=profile.id)

        assert response.status_code == 200
        assert updated_profile.photo
