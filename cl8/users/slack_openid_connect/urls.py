from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import SlackOpenIdConnectProvider

app_name = "slack_openid_connect"
urlpatterns = default_urlpatterns(SlackOpenIdConnectProvider)
