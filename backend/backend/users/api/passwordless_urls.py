from drfpasswordless.settings import api_settings
from django.urls import path
from drfpasswordless.views import (
    ObtainAuthTokenFromCallbackToken,
    VerifyAliasFromCallbackToken,
    ObtainEmailVerificationCallbackToken,
    ObtainEmailCallbackToken
)
from .passwordless_views import ConstellateEmailCallbackToken

urlpatterns = [
    path(
        api_settings.PASSWORDLESS_AUTH_PREFIX + "email/",
        ConstellateEmailCallbackToken.as_view(),
        name="auth_email",
    ),
    path(
        api_settings.PASSWORDLESS_AUTH_PREFIX + "token/",
        ObtainAuthTokenFromCallbackToken.as_view(),
        name="auth_token",
    ),
    path(
        api_settings.PASSWORDLESS_VERIFY_PREFIX + "email/",
        ObtainEmailVerificationCallbackToken.as_view(),
        name="verify_email",
    ),
    path(
        api_settings.PASSWORDLESS_VERIFY_PREFIX,
        VerifyAliasFromCallbackToken.as_view(),
        name="verify_token",
    ),
]
