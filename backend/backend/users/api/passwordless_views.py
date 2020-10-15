import logging

from django.utils.module_loading import import_string
from django.core.mail import send_mail
from django.template import loader
from django.contrib.auth import login
from drfpasswordless.settings import api_settings
from drfpasswordless.utils import (
    create_callback_token_for_user,
    inject_template_context,
    send_sms_with_callback_token,
)
from drfpasswordless import views as drfpwless_views
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def send_email_with_callback_token(user, email_token, **kwargs):
    """
    Sends a Email to user.email.

    Passes silently without sending in test environment
    """
    try:
        if api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS:
            # Make sure we have a sending address before sending.

            # Get email subject and message
            email_subject = kwargs.get(
                "email_subject", api_settings.PASSWORDLESS_EMAIL_SUBJECT
            )
            email_plaintext = kwargs.get(
                "email_plaintext", api_settings.PASSWORDLESS_EMAIL_PLAINTEXT_MESSAGE
            )
            email_html = kwargs.get(
                "email_html", api_settings.PASSWORDLESS_EMAIL_TOKEN_HTML_TEMPLATE_NAME
            )

            # Inject context if user specifies.
            context = inject_template_context(
                {"callback_token": email_token.key, "user": user}
            )
            html_message = loader.render_to_string(email_html, context,)
            send_mail(
                email_subject,
                email_plaintext % email_token.key,
                api_settings.PASSWORDLESS_EMAIL_NOREPLY_ADDRESS,
                [getattr(user, api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME)],
                fail_silently=False,
                html_message=html_message,
            )

        else:
            logger.debug(
                "Failed to send token email. Missing PASSWORDLESS_EMAIL_NOREPLY_ADDRESS."
            )
            return False
        return True

    except Exception as e:  # NOQA: W0703

        logger.debug(
            "Failed to send token email to user: %d."
            "Possibly no email on user object. Email entered was %s"
            % (user.id, getattr(user, api_settings.PASSWORDLESS_USER_EMAIL_FIELD_NAME))
        )
        logger.error(e)
        return False


class RicherContextTokenService:
    @staticmethod
    def send_token(user, alias_type, token_type, **message_payload):
        token = create_callback_token_for_user(user, alias_type, token_type)
        send_action = None
        if alias_type == "email":
            send_action = send_email_with_callback_token
        elif alias_type == "mobile":
            send_action = send_sms_with_callback_token
        # Send to alias
        success = send_action(user, token, **message_payload)
        return success


class ConstellateEmailCallbackToken(drfpwless_views.ObtainEmailCallbackToken):
    """
    This subclass of ObtainEmailCallbackToken works the same way, but
    also allows us to pass more context data into the templates when
    generating a confirmation email, using the RicherContextTokenService.
    """

    def post(self, request, *args, **kwargs):
        if self.alias_type.upper() not in api_settings.PASSWORDLESS_AUTH_TYPES:
            # Only allow auth types allowed in settings.
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            # Validate -
            user = serializer.validated_data["user"]
            # Create and send callback token
            success = RicherContextTokenService.send_token(
                user, self.alias_type, self.token_type, **self.message_payload
            )
            # Respond With Success Or Failure of Sent
            if success:
                status_code = status.HTTP_200_OK
                response_detail = self.success_response
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                response_detail = self.failure_response
            return Response({"detail": response_detail}, status=status_code)
        else:
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )


class ConstellateObtainAuthTokenFromCallbackToken(
    drfpwless_views.ObtainAuthTokenFromCallbackToken
):
    """
    A subclass of ObtainAuthTokenFromCallbackToken. Works the same way, but
    also logs in the user to django, by setting a session cookie, to allow
    authorised users access to the django admin.
    """

    def login_user_for_backend(self, request=None, user=None, backend=None):
        """
        Auth the provided user so the request has the user object added.
        Used to allow staff to login using the email setup, without needing
        to keep track of usernames, or passwords.

        """
        if backend is None:
            backend = "django.contrib.auth.backends.ModelBackend"

        login(request, user, backend=backend)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            token_creator = import_string(api_settings.PASSWORDLESS_AUTH_TOKEN_CREATOR)
            (token, _) = token_creator(user)

            if token:
                TokenSerializer = import_string(
                    api_settings.PASSWORDLESS_AUTH_TOKEN_SERIALIZER
                )
                token_serializer = TokenSerializer(data=token.__dict__, partial=True)
                if token_serializer.is_valid():

                    # this is the one line that differes from
                    # normal ObtainAuthTokenFromCallbackToken.post() method
                    self.login_user_for_backend(request, user)

                    # Return our key for consumption.
                    return Response(token_serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(
                "Couldn't log in unknown user. Errors on serializer: {}".format(
                    serializer.error_messages
                )
            )
        return Response(
            {"detail": "Couldn't log you in. Try again later."},
            status=status.HTTP_400_BAD_REQUEST,
        )

