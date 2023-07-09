import pytest
from allauth.account.models import EmailAddress
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.models import SocialApp, SocialLogin, SocialAccount
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site

from cl8.users.adapters import Cl8SocialAccountAdapter
from cl8.users.models import Profile, User


@pytest.fixture
def return_data():
    """
    Return an example json representation of a sociallogin after successfully
    authenticating against slack
    """
    return {
        "account": {
            "id": None,
            "user_id": None,
            "provider": "slack_openid_connect",
            "uid": "TAAABBBCC_XXXYYYZZZ",
            "last_login": None,
            "date_joined": None,
            "extra_data": {
                "ok": True,
                "sub": "XXXYYYZZZ",
                "https://slack.com/user_id": "XXXYYYZZZ",
                "https://slack.com/team_id": "TAAABBBCC",
                "email": "chris@productscience.co.uk",
                "email_verified": True,
                "date_email_verified": 1621952515,
                "name": "Chris Adams",
                "picture": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_512.jpg",
                "given_name": "Chris",
                "family_name": "Adams",
                "locale": "en-US",
                "https://slack.com/team_name": "ClimateAction.tech",
                "https://slack.com/team_domain": "climate-tech",
                "https://slack.com/user_image_24": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_24.jpg",
                "https://slack.com/user_image_32": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_32.jpg",
                "https://slack.com/user_image_48": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_48.jpg",
                "https://slack.com/user_image_72": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_72.jpg",
                "https://slack.com/user_image_192": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_192.jpg",
                "https://slack.com/user_image_512": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_512.jpg",
                "https://slack.com/user_image_1024": "https://avatars.slack-edge.com/2020-07-21/1276994577392_20c4840e96416dec0782_1024.jpg",
                "https://slack.com/team_image_34": "https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_34.png",
                "https://slack.com/team_image_44": "https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_44.png",
                "https://slack.com/team_image_68": "https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_68.png",
                "https://slack.com/team_image_88": "https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_88.png",
                "https://slack.com/team_image_102": "https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_102.png",
                "https://slack.com/team_image_132": "https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_132.png",
                "https://slack.com/team_image_230": "https://avatars.slack-edge.com/2020-07-20/1251887364371_d524a7bf9c23d189f5a3_230.png",
                "https://slack.com/team_image_default": False,
            },
        },
        "user": {
            "id": None,
            "password": "!zXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "last_login": None,
            "is_superuser": False,
            "username": "",
            "first_name": "Chris",
            "last_name": "Adams",
            "email": "chris@productscience.co.uk",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2023-07-08T20:55:45.862Z",
            "name": "",
        },
        "state": {"next": "/", "process": "login", "scope": "", "auth_params": ""},
        "email_addresses": [
            {
                "id": None,
                "user_id": None,
                "email": "chris@productscience.co.uk",
                "verified": True,
                "primary": True,
            }
        ],
        "token": {
            "id": None,
            "app_id": None,
            "account_id": None,
            "token": "xoxp-123451234512-123451234512-1234512345123-deadbeefdeadbeefdeadbeefdeadbeef",  # noqa
            "token_secret": "",
            "expires_at": None,
        },
    }


@pytest.fixture
def allauth_social_slack_app() -> SocialApp:
    site = Site.objects.get()

    # and social login set up
    social_app = SocialApp.objects.create(
        name="CAT Slack",
        provider="slack",
        secret="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        client_id="xxxxxxxxxxxx.xxxxxxxxxxxxx",
    )
    social_app.sites.add(site)
    social_app.save()
    return social_app


@pytest.mark.django_db
def test_signing_in_via_slack_with_no_existing_user(
    rf, mocker, return_data: dict, allauth_social_slack_app: SocialApp
):
    """
    Test that a user who does not yet exist in a constellation, but is a member of
    the linked slack workspace is able to login, and the correct profile
    information is created.
    """
    # create our adapter for simulating login
    adapter = Cl8SocialAccountAdapter()
    mocker.patch(
        "allauth.socialaccount.models.SocialLogin.serialize", return_value=return_data
    )
    # when a user logs in via slack sign in
    # make a fake social login
    req = rf.get("/accounts/slack_openid_connect/login/callback/")

    # django RequestFactories by default do not support sessions, so we have to
    # add support for them ourselves by calling `process_request` the middleware
    # that our social login relies on. This mutates the request the way middleware
    # would do in a live running server

    req.user = AnonymousUser()
    SessionMiddleware(lambda request: None).process_request(req)
    assert not req.user.is_authenticated

    # simulate the parsing of the login data in the normal flow when
    # hitting the callback endpoint. Doing it this way means we don't
    # need to mock out so much of the complicated oauth flow. In the
    # normal flow, a sociallogin is created from the return data, so we
    # do the same here
    sociallogin = SocialLogin.deserialize(return_data)
    try:
        adapter.pre_social_login(req, sociallogin)
    except ImmediateHttpResponse:
        pass

    # then the user is created
    assert User.objects.all().count() == 1
    eml = return_data["email_addresses"][0]["email"]
    user = User.objects.get(email=eml)

    # and their profile is created too
    assert Profile.objects.all().count() == 1

    # and the email addresses are created the way allauth
    # expects them to be
    assert EmailAddress.objects.all().count() == 1
    assert eml == EmailAddress.objects.first().email

    # and they appear as logged in
    assert req.user.is_authenticated
    assert req.user == user

    # and finally the corresponding social account is stored locally
    assert SocialAccount.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_signing_in_via_slack_with_existing_user_but_no_previous_signin(
    rf,
    mocker,
    return_data,
    fake_photo_profile_factory,
    user_factory,
    allauth_social_slack_app: SocialApp,
):
    """
    Test that a user who already exists in constellation and has the same email
    address as that provided by slack can be logged in, and the correct profile
    information is created.
    See test_signing_in_via_slack_with_no_existing_user for comments about specific
    sections of code
    """

    # given a user with a profile
    # who has the same email address as a provided slack profile
    user = user_factory.create(email="chris@productscience.co.uk")
    slack_profile = return_data["account"]["extra_data"]
    slack_user_id = slack_profile["https://slack.com/user_id"]
    slack_name = slack_profile["name"]
    slack_import_id = f"slack-{slack_user_id}"
    profile = fake_photo_profile_factory.create(user=user, import_id=slack_import_id)

    assert User.objects.all().count() == 1

    # when they log in via slack sign in
    adapter = Cl8SocialAccountAdapter()
    mocker.patch(
        "allauth.socialaccount.models.SocialLogin.serialize", return_value=return_data
    )
    # when a user logs in via slack sign in
    # make a fake social login
    req = rf.get("/accounts/slack_openid_connect/login/callback/")

    # create our non-signed in request
    req.user = AnonymousUser()
    SessionMiddleware(lambda request: None).process_request(req)
    assert not req.user.is_authenticated

    # log our user in
    sociallogin = SocialLogin.deserialize(return_data)
    try:
        adapter.pre_social_login(req, sociallogin)
    except ImmediateHttpResponse:
        pass

    # assert that the number of users is the same
    # and the user is the same
    assert User.objects.all().count() == 1

    eml = return_data["email_addresses"][0]["email"]
    assert user == User.objects.get(email=eml)
    assert user.email == eml

    # and their profile is created too
    assert Profile.objects.all().count() == 1
    assert profile == Profile.objects.first()

    # but the profile has not been overridden
    # this preserves changes made to the directory, so
    # if a user updates their name in the directory it is
    # not overridden
    profile_from_db = Profile.objects.first()
    assert profile_from_db.name == user.name
    # user.name should not be overriden by slack_name the user nane
    # is already set
    assert user.name != slack_name

    # and the email addresses are created the way allauth
    # expects them to be
    assert EmailAddress.objects.all().count() == 1
    assert eml == EmailAddress.objects.first().email

    # and they appear as logged in
    assert req.user.is_authenticated
    assert req.user == user


@pytest.mark.django_db
def test_signing_in_via_slack_with_existing_user_and_previous_signin(
    rf,
    mocker,
    return_data,
    fake_photo_profile_factory,
    user_factory,
    allauth_social_slack_app: SocialApp,
):
    """
    Test that a user who has signed in once, can sign on subsequent occasions.
    We need this because with allauth on the first sign in stores information in
    the local database that must be unique.

    """

    # given a user with a profile
    # who has the same email address as a provided slack profile
    user = user_factory.create(email="chris@productscience.co.uk")
    slack_profile = return_data["account"]["extra_data"]
    slack_user_id = slack_profile["https://slack.com/user_id"]
    slack_import_id = f"slack-{slack_user_id}"
    fake_photo_profile_factory.create(user=user, import_id=slack_import_id)

    assert User.objects.all().count() == 1

    # when they log in via slack sign in
    adapter = Cl8SocialAccountAdapter()
    mocker.patch(
        "allauth.socialaccount.models.SocialLogin.serialize", return_value=return_data
    )
    # when a user logs in via slack sign in
    # make a fake social login
    req = rf.get("/accounts/slack_openid_connect/login/callback/")

    # create our non-signed in request
    req.user = AnonymousUser()
    SessionMiddleware(lambda request: None).process_request(req)
    assert not req.user.is_authenticated

    # log our user in
    sociallogin = SocialLogin.deserialize(return_data)
    try:
        adapter.pre_social_login(req, sociallogin)
    except ImmediateHttpResponse:
        pass

    # when a user logs in via slack sign in the second time
    req = rf.get("/accounts/slack_openid_connect/login/callback/")
    req.user = AnonymousUser()
    SessionMiddleware(lambda request: None).process_request(req)
    assert not req.user.is_authenticated

    # log our user in
    sociallogin = SocialLogin.deserialize(return_data)
    try:
        adapter.pre_social_login(req, sociallogin)
    except ImmediateHttpResponse:
        pass

    assert req.user.is_authenticated
