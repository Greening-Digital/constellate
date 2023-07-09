from typing import Any, List, Union

from allauth.account.models import EmailAddress
from allauth.exceptions import ImmediateHttpResponse
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialLogin, SocialAccount
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import redirect

from ..utils.pics import fetch_user_pic
from .models import Profile, User


class AccountAdapter(DefaultAccountAdapter):
    """
    An override of the Default account adapter, so support changing
    whether registration is supported.
    """

    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class Cl8SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    An extension of the DefaultSocialAccountAdapter, where we make explicit
    how we handle the data returned from slack, and how we persist to the User
    Profile models in our database
    """

    EMAIL_REQUIRED = False

    def _complete_login_for_slack(
        self, slack_data: dict, sociallogin: SocialLogin
    ) -> List[Union[User, SocialLogin, Profile]]:
        """
        Accept the data payload from slack, and create the necessary users,
        social logins
        """
        # fetch our info out of the data payload from slack
        slack_profile = slack_data["account"]["extra_data"]
        slack_user_id = slack_profile["https://slack.com/user_id"]
        slack_photo = slack_profile["https://slack.com/user_image_512"]
        slack_email = slack_data["user"]["email"]
        slack_import_id = f"slack-{slack_user_id}"
        slack_name = slack_profile["name"]

        # create our user, and populate with info that our profile uses,
        # along with a helpful username
        user, user_created = User.objects.get_or_create(email=slack_email)
        if user_created:
            user.first_name = slack_profile["given_name"]
            user.last_name = slack_profile["family_name"]
            user.name = slack_profile["name"]
            user.username = f"{slack_name} - {slack_user_id}"
            user.save()

        # create an email address as allauth expects
        eml, _ = EmailAddress.objects.get_or_create(
            email=slack_data["email_addresses"][0]["email"], user=user
        )

        # get or create our profile, adding the correct photo and name
        prof, prof_created = Profile.objects.get_or_create(
            import_id=slack_import_id, user=user
        )

        if prof_created:
            prof.photo = fetch_user_pic(slack_photo)
            prof.user = user
            # TODO: fetch info from google sheets
            prof.save()
            user.save()

        return [user, sociallogin, prof]

    def pre_social_login(self, request, sociallogin):
        """
        An override of the default social login flow, to
        connect a user to their corresponding profile that they signed up with.
        """

        returned_profile = sociallogin.serialize()
        returned_social_uid = returned_profile["account"]["uid"]
        # handle the case of using slack as a login mechanism. We only have one social login now,
        # so there is no check
        user, sociallogin, profile = self._complete_login_for_slack(
            returned_profile, sociallogin
        )

        # connect the user to the social sign in for an easier sign-in later

        social_account_exists = SocialAccount.objects.filter(
            uid=returned_social_uid
        ).exists()

        if not social_account_exists:
            sociallogin.connect(request, user)

        login(request, user, "allauth.account.auth_backends.AuthenticationBackend")

        # in the normal allauth flow with social signin,
        # `allauth.socialaccount.helpers.complete_social_login` calls
        # `pre_social_login`, and catches the `ImmediateHttpResponse`
        # exception to continue it's flow. So, we raise an exception
        # instead of returning
        raise ImmediateHttpResponse(redirect("home"))

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
