import requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


from .provider import SlackOpenIdConnectProvider


class SlackOpenIdConnectAdapter(OAuth2Adapter):
    """
    An updated slack adapter designed to use the updated openid connect
    flow as opposed to the deprecated auth2, identity-based flow.
    """

    # setting thids idea
    provider_id = SlackOpenIdConnectProvider.id

    access_token_url = "https://slack.com/api/openid.connect.token"
    identity_url = "https://slack.com/api/openid.connect.userInfo"
    authorize_url = "https://slack.com/openid/connect/authorize"

    # # we allow for an override here, to set a subdomain
    # if settings.SLACK_SIGNIN_AUTHORIZE_URL:
    # authorize_url = settings.SLACK_SIGNIN_AUTHORIZE_URL

    def complete_login(self, request, app, token, **kwargs):
        """
        Return a sociallogin from slack, with empty user
        """
        extra_data = self.get_data(token.token)
        sociallogin = self.get_provider().sociallogin_from_response(request, extra_data)
        return sociallogin

    def get_data(self, token):
        """
        Overrides the default behaviour to conform to the new spec
        needed for the slack server.
        Returns a JSON payload describing the slack user

        """
        hed = {"Authorization": "Bearer " + token}
        resp = requests.get(self.identity_url, headers=hed)
        resp = resp.json()

        if not resp.get("ok"):
            raise OAuth2Error()

        return resp


oauth2_login = OAuth2LoginView.adapter_view(SlackOpenIdConnectAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(SlackOpenIdConnectAdapter)
