from cl8.users.importers import safe_username
from typing import Any
import io
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest
from django.shortcuts import redirect
from .models import Profile
from ..utils.pics import fetch_user_pic


import requests
from django.core.files.images import ImageFile


from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.utils import user_email, user_field, user_username

from allauth.socialaccount.signals import social_account_updated, social_account_added
from allauth.account.signals import user_signed_up

from django.dispatch import receiver


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


from .importers import safe_username


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    An extension of the DefaultSocialAccountAdapter, where we make explicit
    how we handle the data returned from slack, and how we persist to the User
    Profile models in our database
    """

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


@receiver(user_signed_up)
def create_profile_for_user(sender, **kwargs):
    """Called when a user signs in via slack for the first time"""
    update_profile(sender, **kwargs)


@receiver(social_account_updated)
def update_profile_for_user(sender, **kwargs):
    """Called when a user signs in via slack for the each subsequent time"""
    update_profile(sender, **kwargs)


def update_profile(sender, **kwargs):
    """
    Accept a payload of info from the allauth signal events for
    creating a user via a social sign in, or signing in using slack.

    """
    sociallogin = kwargs.get("sociallogin")

    # return early if this isn't a social login event
    if not sociallogin:
        return

    # TODO: decide how to map existing sociallogin to an existing user
    # with a profile matching the the provided email address.

    # add a profile if one does not already exist for a given user
    if not sociallogin.user.has_profile():
        # extra the profile
        slack_user_id = sociallogin.account.extra_data["https://slack.com/user_id"]
        slack_photo_url = sociallogin.account.extra_data["picture"]
        user = sociallogin.user

        user.username = f"{user.first_name.lower()}-{slack_user_id}"
        user.name = f"{user.first_name} {user.last_name}"
        user.save()

        prof = Profile.objects.create(
            user=user,
            name=user.name,
            import_id=f"slack-{slack_user_id}",
        )

        photo = fetch_user_pic(slack_photo_url)
        prof.photo.save(f"{sociallogin.user}_slack_pic", photo)
        prof.save()
