import pytest
from django.core.files.images import ImageFile


from cl8.users.api.serializers import ProfilePicSerializer, ProfileSerializer
from cl8.users.models import Profile, User

pytestmark = pytest.mark.django_db


class TestProfileSerializer:
    @pytest.mark.parametrize("photo_size", [("thumbnail_photo"), ("detail_photo")])
    def test_profile_with_photo(self, fake_photo_profile: Profile, photo_size):

        ps = ProfileSerializer(fake_photo_profile)
        assert photo_size in ps.data.keys()

    def test_create_profile_data(self):

        profile_dict = {
            # these are the bits we need to create for end users,
            # before putting them back in the returned
            "name": "Joe Bloggs",
            "email": "person@email.com",
            "phone": "9329275526",
            "website": "http://livingston.biz",
            "twitter": "paul58",
            "facebook": "fday",
            "linkedin": "wpalmer",
            "organisation": "Acme Inc",
            "tags": ["tech"],
            "bio": "Themselves TV western under. Tv can beautiful we throughout politics treat both. Fear speech left get answer over century.",
            "visible": False,
            "admin": True,
        }

        ps = ProfileSerializer(data=profile_dict)
        assert ps.is_valid()

        res = ps.create(ps.data)
        user = User.objects.get(email=profile_dict["email"])

        new_ps = ProfileSerializer(res)
        new_data = new_ps.data

        assert "id" in new_data.keys()

        assert "thumbnail_photo" in new_data.keys()
        assert "detail_photo" in new_data.keys()
        assert new_data["name"] == user.name
        assert new_data["email"] == user.email

    def test_update_profile_data(self, profile):

        # import ipdb ; ipdb.set_trace()

        profile_dict = {
            "name": "A New Name",
            "phone": profile.phone,
            "website": profile.website,
            "twitter": profile.twitter,
            "facebook": profile.facebook,
            "linkedin": profile.linkedin,
            "organisation": profile.organisation,
            "bio": "something new",
            "visible": profile.visible,
            "admin": True,
        }

        ps = ProfileSerializer(data=profile_dict)
        assert ps.is_valid()

        res = ps.update(profile, ps.data)
        res_data = ProfileSerializer(res)

        updated_user = User.objects.get(email=profile.user.email)

        # have we updated our user details?
        assert updated_user.name == profile_dict["name"]
        assert updated_user.is_staff == profile_dict["admin"]

        # and has the profile been updated?
        assert res.bio == profile_dict["bio"]

    def test_update_profile_tags(self, profile):
        """
        Given
        """

        assert profile.tags.count() == 0

        profile_dict = {
            "tags": ["tech"],
        }

        ps = ProfileSerializer(data=profile_dict)
        assert ps.is_valid()

        res = ps.update(profile, ps.data)
        new_ps = ProfileSerializer(res)
        new_data = new_ps.data

        assert res.tags.first().name == "tech"


class TestProfilePicSerializer:
    def test_serialise_existing_profile(self, profile):
        pro = ProfilePicSerializer(profile)
        assert pro.data["id"] == profile.id
        assert pro.data["photo"] == profile.photo

    @pytest.mark.only
    def test_validate_profile_pic_submission(self, profile, tmp_pic_path):
        """
        Given an valid profile with an id, and an valid image, we have a valid submission.
        """

        # we need a file_object to pass into our ImageFile for django to
        # recognise it as a file. We opening a real file, rather than
        # making a binary BytesIO ourselves, means we can easily view the file
        test_pic = open(tmp_pic_path, "rb")
        upload_file = ImageFile(test_pic, name="test_pic.png")

        # simulate our django file and profile id being submitted via the API
        ps = ProfilePicSerializer(data={"id": profile.id, "photo": upload_file})

        assert ps.is_valid()
        assert "id" in ps.validated_data
        assert "photo" in ps.validated_data

    def test_validate_profile_pic_submission_no_pic(
        self, profile,
    ):
        """
        Given an valid profile with an id, but no image, our serialiser catches
        the invalid submission.
        """

        # simulate our django file and profile id being submitted via the API
        ps = ProfilePicSerializer(data={"id": profile.id, "photo": None})

        assert not ps.is_valid()
