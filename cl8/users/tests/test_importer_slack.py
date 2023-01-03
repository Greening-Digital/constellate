import pytest
from .. import importers, models

import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


@pytest.fixture
def slack_dummy_user():
    return {
        "ok": True,
        "user": {
            "id": "UXXXXXXXX",
            "team_id": "XXXXXXXXX",
            "name": "chris",
            "deleted": False,
            "color": "df3dc0",
            "real_name": "Chris Adams",
            "tz": "Europe/Amsterdam",
            "tz_label": "Central European Summer Time",
            "tz_offset": 7200,
            "profile": {
                "title": "",
                "phone": "",
                "skype": "",
                "real_name": "Chris Adams",
                "real_name_normalized": "Chris Adams",
                "display_name": "mrchrisadams",
                "display_name_normalized": "mrchrisadams",
                "fields": None,
                "status_text": "some text",
                "status_emoji": ":some_emoji:",
                "status_expiration": 0,
                "avatar_hash": "20c4840e9641",
                "image_original": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_original.jpg",
                "is_custom_image": True,
                "email": "chris@productscience.co.uk",
                "first_name": "Chris",
                "last_name": "Adams",
                "image_24": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_24.jpg",
                "image_32": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_32.jpg",
                "image_48": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_48.jpg",
                "image_72": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_72.jpg",
                "image_192": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_192.jpg",
                "image_512": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_512.jpg",
                "image_1024": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_1024.jpg",
                "status_text_canonical": "",
                "team": "XXXXXXXXX",
            },
            "is_admin": True,
            "is_owner": True,
            "is_primary_owner": False,
            "is_restricted": False,
            "is_ultra_restricted": False,
            "is_bot": False,
            "is_app_user": False,
            "updated": 1614874162,
            "is_email_confirmed": True,
        },
    }


class TestSlackImporter:
    @pytest.mark.smoke_test
    def test_fetch_users(self, db, profile, slack_dummy_user, mocker):
        """
        Test that we can fetch the list of users, or user ids in a given public channel
        """

        # set our email to we expect to have returned in data
        # by our calls to the slack API
        # profile.user.email = "chris@productscience.co.uk"
        profile.import_id = "slack-UXXXXXXXX"
        # profile.user.save()
        profile.save()
        # we expect to get back a list of IDs, but none of the IDs should match our
        # dummy slack user, so we monkey patch the class to avoid making network calls

        # first patch the initialise call for the the web client for slack
        mocker.patch(
            "cl8.users.importers.SlackImporter.__init__", return_value=None,
        )
        # then patch the method we use to fetch a list of users back using the
        # underlying slack API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_ids",
            return_value=["UCM06DU1K"],
        )
        # call our mocked methods to hae a result to check against
        importer = importers.SlackImporter()
        res = importer.list_new_users()

        # do we have any results?
        assert len(res) > 0
        import_ids = models.Profile.objects.all().values_list("import_id", flat=True)

        # have we filtered for already existing users?
        for id in res:
            logger.info(f"slack-{id}")
            assert f"slack-{id}" not in import_ids

    @pytest.mark.smoke_test
    def test_fetch_users_without_dupes(self, db, profile, mocker, slack_dummy_user):
        """
        Test that we can fetch the list of users, or user ids in a given public channel
        """

        # first patch the initialise call for the the web client for slack
        mocker.patch(
            "cl8.users.importers.SlackImporter.__init__", return_value=None,
        )
        # then patch the method we use to fetch a list of users back using the
        # underlying slack API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_ids",
            return_value=["UCM06DU1K"],
        )
        # return the user as if we had fetched it from the API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_for_id",
            return_value=slack_dummy_user["user"],
        )

        # set our email to we expect to have returned in data
        # by our calls to the slack API
        # profile.user.email = "chris@productscience.co.uk"
        # we expect to get back a list of IDs, but none of the IDs
        importer = importers.SlackImporter()
        res = importer.list_new_users()

        imported_id = res[0]

        profile.import_id = imported_id
        profile.save()

        updated_res = importer.list_new_users()

        # do we have any results?
        assert len(updated_res) < len(res)
        assert imported_id not in updated_res

    def test_import_user(self, db, mocker, slack_dummy_user):
        """
        Given: a mocked slack client and a dummy payload
        Then: create a user and profile, stored in the database
        """

        # first patch the initialise call for the the web client for slack
        mocker.patch(
            "cl8.users.importers.SlackImporter.__init__", return_value=None,
        )
        # then patch the method we use to fetch a list of users back using the
        # underlying slack API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_ids",
            return_value=["UCM06DU1K"],
        )
        # return the user as if we had fetched it from the API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_for_id",
            return_value=slack_dummy_user["user"],
        )

        importer = importers.SlackImporter()
        res = importer._fetch_user_ids()

        user_id = res[0]
        user_from_api = importer._fetch_user_for_id(user_id)
        imported_user = importer.import_slack_user(user_id)

        # email
        assert imported_user.email == user_from_api["profile"]["email"]
        assert imported_user.profile.email == user_from_api["profile"]["email"]

        # slack_id
        assert imported_user.profile.import_id == f"slack-{user_from_api['id']}"

        # display_name_normalized -
        assert (
            imported_user.profile.name
            == user_from_api["profile"]["real_name_normalized"]
        )

        # do we now have a photo?
        # import rich
        # rich.inspect(slack_dummy_user)
        # logger.info(slack_dummy_user[])
        # assert imported_user.profile.photo.url is not None

        # use this as a sanity check
        # import webbrowser
        # webbrowser.open(imported_user.profile.photo.path)

    @pytest.mark.smoke_test
    def test_import_users(self, db, mocker, slack_dummy_user):
        """
        Smoke test for running an import
        """

        # first patch the initialise call for the the web client for slack
        mocker.patch(
            "cl8.users.importers.SlackImporter.__init__", return_value=None,
        )
        # then patch the method we use to fetch a list of users back using the
        # underlying slack API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_ids",
            return_value=["UXXXXXXXX"],
        )
        # return the user as if we had fetched it from the API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_for_id",
            return_value=slack_dummy_user["user"],
        )

        # pass
        importer = importers.SlackImporter()
        first_run_users = importer.import_users()

        #
        assert len(first_run_users) > 0

    @pytest.mark.smoke_test
    def test_import_users_idempotent(self, db, mocker, slack_dummy_user):
        """
        Check that we can run this importer repeatedly,
        without making multiples of profiles or users.

        This lets us run the import on a cronjob, or expose
        an HTTP enpdpoint if sensible.
        """
        # first patch the initialise call for the the web client for slack
        mocker.patch(
            "cl8.users.importers.SlackImporter.__init__", return_value=None,
        )
        # then patch the method we use to fetch a list of users back using the
        # underlying slack API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_ids",
            return_value=["UXXXXXXXX"],
        )
        # return the user as if we had fetched it from the API
        mocker.patch(
            "cl8.users.importers.SlackImporter._fetch_user_for_id",
            return_value=slack_dummy_user["user"],
        )

        importer = importers.SlackImporter()

        first_run = importer.import_users()
        second_run = importer.import_users()

        assert len(first_run) > len(second_run)
