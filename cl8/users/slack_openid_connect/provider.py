from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.slack.provider import SlackAccount

from allauth.account.models import EmailAddress

# SlackOpenIdConnectProvider


class SlackProvider(OAuth2Provider):
    """
    An updated subclass of the slack provider,
    that uses the the newer OpenID connect flow
    for sign-in .
    """

    id = "slack_openid_connect"
    name = "Slack Open ID Connect"
    account_class = SlackAccount

    def extract_uid(self, data):
        """
        Extract the UID using using the updated openid connect keys.
        """
        team_id = str(data.get("https://slack.com/team_id"))
        user_id = str(data.get("https://slack.com/user_id"))

        return f"{team_id}_{user_id}"

    def extract_common_fields(self, data):
        return {
            "name": data.get("name"),
            "first_name": data.get("given_name"),
            "last_name": data.get("family_name"),
            "email": data.get("email", None),
        }

    def extract_email_addresses(self, data):
        """
        Create email address object for the given user, to persist
        to the database for them.
        """
        return [
            EmailAddress(
                email=data.get("email"),
                verified=data.get("email_verified"),
                primary=True,
            )
        ]
        # breakpoint()
        # return []

    def get_default_scope(self):
        return ["openid", "email", "profile"]


provider_classes = [SlackProvider]
