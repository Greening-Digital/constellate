import webbrowser

import pytest
from django.contrib.sites.models import Site

from ..models import Constellation, Profile, User  # noqa

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_site():
    # sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Site])
    # with connection.cursor() as cursor:
    #     for sql in sequence_sql:
    #     cursor.execute(sql)
    # https://stackoverflow.com/questions/14589634/how-to-reset-the-sequence-for-ids-on-postgresql-tables

    # https://code.djangoproject.com/ticket/17415

    from django.core.management.color import no_style
    from django.db import connection

    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Site])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)

    # Site.objects.first().save()

    # woo = Site.objects.create(domain="woop.com", name="woop")

    return Site.objects.create(name="Sample Site", domain="testserver")


def view_rendered_html_in_browser(string_template):
    """
    Accepts a string, containing generated HTML template
    then opens it in the default browser on a computer
    """

    # show the rendered html
    with open("email_test.html", "w+") as f:
        f.write(string_template)

    webbrowser.open("email_test.html")


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"


class TestProfile:
    def test_user_profile(self, profile: Profile):
        assert profile.email == profile.user.email

    def test_check_for_admin_status(self, profile: Profile):
        profile.user.is_staff = True
        profile.save()

        assert profile.admin is True

    @pytest.mark.parametrize("photo_size", [("thumbnail_photo"), ("detail_photo")])
    def test_profile_photo_thumbs(
        self, fake_photo_profile: Profile, settings, photo_size
    ):
        pic_url = getattr(
            fake_photo_profile,
            photo_size,
        )

        # is this pointing to the correct directory where our media is stored?
        assert settings.MEDIA_URL in pic_url

    def test_send_invite_for_profile(
        self, profile: Profile, mailoutbox, test_constellation
    ):
        profile.send_invite_mail()
        assert len(mailoutbox) == 1

    def test_generate_invite_for_profile(
        self, profile: Profile, mailoutbox, test_constellation
    ):
        rendered_templates = profile.generate_invite_mail()

        # uncomment this to view the rendered mjml/html template
        # view_rendered_html_in_browser(rendered_templates["html"])
        # uncomment this to view the rendered text template
        # view_rendered_html_in_browser(rendered_templates["text"])

        assert "html" in rendered_templates
        assert "text" in rendered_templates

    def test_clusters_as_tags(self, profile: Profile):
        """
        We represent clusters as tags,
        """

        profile.clusters.add("Open Energy")
        profile.save()

        assert "Open Energy" in [tag_name for tag_name in profile.clusters.names()]

    def test_vcard(self, profile: Profile):
        vcard = profile.vcard()

        assert vcard.fn.value == profile.name
        assert vcard.email.value == profile.email
        assert vcard.phone.value == profile.phone
        assert vcard.url.value == profile.website
        assert vcard.org.value == profile.organisation


class TestSiteProfile:
    def test_site_profile(self):
        """
        Test that a site can have a profile set
        """
        pass

    def test_site_profile_logo(self, sample_site, tmp_pic_path):
        """
        Test site profile, can have a user defined image, that can be shown in the UI
        """

        constellation = Constellation(site=sample_site)
        constellation.save()

        # add our profile logo.

        # test that we can access a url for the logo

        # import ipdb ; ipdb.set_trace()
