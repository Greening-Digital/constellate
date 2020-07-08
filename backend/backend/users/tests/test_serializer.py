import pytest
from django.test import RequestFactory

from backend.users.api.views import ProfileViewSet
from backend.users.models import User, Profile
from backend.users.api.serializers import ProfileSerializer
from backend.users.tests.factories import ProfileFactory

pytestmark = pytest.mark.django_db


class TestProfileSerializer:

    @pytest.mark.only
    def test_create_profile_data(self, user):

        # profile_data = ProfileFactory(
        user.save()

        profile_dict = {
            # these are the bits we need to create for end users, before putting them back in the returned
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

        res = ps.create(ps.data, user=user)

        for key in ['name', 'email']:
            assert getattr(res, key)
            assert getattr(res, key) == getattr(user, key)
