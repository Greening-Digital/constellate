import pytest
from django.test import RequestFactory

from backend.users.api.views import ProfileViewSet
from backend.users.models import User, Profile
from backend.users.api.serializers import ProfileSerializer
from backend.users.tests.factories import ProfileFactory

pytestmark = pytest.mark.django_db


class TestProfileSerializer:

    # def test_detail_with_photo(self, profile):


    @pytest.mark.only
    def test_create_profile_data(self):

        # profile_data = ProfileFactory(
        # user.save()

        profile_dict = {
            # these are the bits we need to create for end users, before putting them back in the returned
            "name": "Joe Bloggs",
            "email": "person@email.com",

            'phone': '9329275526',
            'website': 'http://livingston.biz',
            'twitter': 'paul58',
            'facebook': 'fday',
            'linkedin': 'wpalmer',

            'tags': ["tech"],

            'bio': 'Themselves TV western under. Tv can beautiful we throughout politics treat both. Fear speech left get answer over century.',

            'visible': False,
            'admin': True,
        }

        ps = ProfileSerializer(data=profile_dict)
        assert ps.is_valid()

        res = ps.create(ps.data)
        user = User.objects.get(email=profile_dict['email'])

        new_ps = ProfileSerializer(res)
        new_data = new_ps.data

        assert 'id' in new_data.keys()
        assert 'photo' in new_data.keys()
        assert new_data['name'] == user.name
        assert new_data['email'] == user.email


    def test_update_profile_data(self, profile):

        # import ipdb ; ipdb.set_trace()

        profile_dict = {
            'phone': profile.phone,
            'website': profile.website,
            'twitter': profile.twitter,
            'facebook': profile.facebook,
            'linkedin': profile.linkedin,
            'bio': profile.bio,

            'visible': profile.visible,
            'admin': profile.admin
        }

        ps = ProfileSerializer(data=profile_dict)

        res = ps.update(profile, ps.data)

        import ipdb ; ipdb.set_trace()
        assert 'id' in new_data.keys()
        assert 'photo' in new_data.keys()
        assert new_data['name'] == user.name
        assert new_data['email'] == user.email