import pytest
from django.template.loader import render_to_string
import webbrowser

def view_rendered_html_in_browser(string_template):
    """
    Accepts a string, containing generated HTML template
    then opens it in the default browser on a computer
    """

    # show the rendered html
    with open("email_test.html", "w+") as f:
        f.write(string_template)

    webbrowser.open("email_test.html")

class TestTemplateEmail:

    @pytest.mark.only
    def test_render_email(self):

        ctx = {
            "callback_token": 272100,
            "support_email_address": "email@domain.com"
        }

        rendered_html = render_to_string(
            "passwordless_default_token_email.html",
            context=ctx
        )

        # uncomment this to view the rendered mjml/html template
        # view_rendered_html_in_browser(rendered_html)

        assert len(rendered_html) > 0
        assert str(ctx['callback_token']) in rendered_html
        assert str(ctx['support_email_address']) in rendered_html

