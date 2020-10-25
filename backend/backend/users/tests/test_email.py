import pytest
from django.template.loader import render_to_string
import webbrowser
from rest_framework.test import RequestsClient, APIClient


def view_rendered_html_in_browser(string_template):
    """
    Accepts a string, containing generated HTML template
    then opens it in the default browser on a computer
    """

    # show the rendered html
    with open("email_test.html", "w+") as f:
        f.write(string_template)

    webbrowser.open("email_test.html")


@pytest.mark.django_db
class TestTemplateEmail:
    def test_render_email(self, profile):
        """
        Test that the tempalte renders with based on what we're passing into context.
        This doesn't test how we add varaibles into the context though.
        """

        ctx = {
            "callback_token": 272100,
            "support_email_address": "email@domain.com",
            "user": profile.user,
        }

        rendered_html = render_to_string(
            "passwordless_default_token_email.mjml.html", context=ctx
        )

        # uncomment this to view the rendered mjml/html template
        # view_rendered_html_in_browser(rendered_html)

        assert len(rendered_html) > 0
        assert str(ctx["callback_token"]) in rendered_html
        assert str(ctx["support_email_address"]) in rendered_html
        assert str(profile.name) in rendered_html

    @pytest.mark.django_db
    def test_add_context(self, profile, mailoutbox):
        """

        """

        # post to the new token send point
        assert len(mailoutbox) == 0
        client = APIClient()
        res = client.post("http://testserver/auth/email/", {"email": profile.email})
        email_html = mailoutbox[0].alternatives[0][0]
        # view_rendered_html_in_browser(email_html)
        assert profile.name in email_html
        assert len(mailoutbox) == 1
