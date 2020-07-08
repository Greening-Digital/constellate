import pytest
from django.test import RequestFactory

from backend.users.api.views import ProfileViewSet
from backend.users.models import User, Profile
from backend.users.api.serializers import ProfileSerializer
from backend.users.tests.factories import ProfileFactory

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
        ]:
            assert response.data[prop] == getattr(profile, prop)

        # we need to check separately for tags, as they use
        # their own manager
        response.data['tags'] = [tag for tag in profile.tags.all()]


    @pytest.mark.only
    def test_data_structure(self, profile: Profile, rf: RequestFactory):
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


    @pytest.mark.skip(reason="not implemented")
    def test_create_profile(self, profile: Profile, rf: RequestFactory):
        view = ProfileViewSet()
        request = rf.get("/fake-url/")
        request.user = profile.user

        assert 1 == 2

        # profile_data = ProfileFactory()

        # profile_dict = {
        #     'id': 4598,
        #     'user_id': 5768,
        #     'phone': '9329275526',
        #     'website': 'http://livingston.biz',
        #     'twitter': 'paul58',
        #     'facebook': 'fday',
        #     'linkedin': 'wpalmer',
        #     'email': 'email@somesite.com',
        #     'tags': ["tech"],
        #     'bio': 'Themselves TV western under. Tv can beautiful we throughout politics treat both. Fear speech left get answer over century.',
        #     'visible': False,
        # }

        # ps = ProfileSerializer(data=profile_dict)
        # import ipdb ; ipdb.set_trace()


        # response = view.create(request)

        # assert respones.status_code == 201
