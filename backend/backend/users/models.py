from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models import CharField
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import get_thumbnail
from taggit.managers import TaggableManager
from taggit.models import TagBase, TaggedItemBase


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Cluster(TagBase):
    class Meta:
        verbose_name = _("Cluster")
        verbose_name_plural = _("Clusters")


class TaggedCluster(TaggedItemBase):
    content_object = models.ForeignKey("Profile", on_delete=models.CASCADE)

    tag = models.ForeignKey(
        Cluster, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_items",
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(_("phone"), max_length=254, blank=True, null=True)
    website = models.URLField(_("website"), max_length=200, blank=True, null=True)
    organisation = models.CharField(
        _("organisation"), max_length=254, blank=True, null=True
    )
    twitter = models.CharField(_("twitter"), max_length=254, blank=True, null=True)
    facebook = models.CharField(_("facebook"), max_length=254, blank=True, null=True)
    linkedin = models.CharField(_("linkedin"), max_length=254, blank=True, null=True)
    bio = models.TextField(_("bio"), blank=True, null=True)
    visible = models.BooleanField(_("visible"), default=False)
    photo = models.ImageField(_("photo"), blank=True, null=True, max_length=200)

    tags = TaggableManager(blank=True)
    clusters = TaggableManager("Clusters", blank=True, through=TaggedCluster)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ["user__name"]

    @property
    def name(self):
        return self.user.name

    @property
    def email(self):
        return self.user.email

    @property
    def admin(self):
        return self.user.is_staff

    @property
    def thumbnail_photo(self):
        if not self.photo:
            return None

        return get_thumbnail(self.photo, "100x100", crop="center", quality=99).url

    @property
    def detail_photo(self):
        """
        A photo, designed for showing on a page, when viewing a profile, with
        a user's details

        """
        if not self.photo:
            return None

        return get_thumbnail(self.photo, "250x250", crop="center", quality=99).url

    def __str__(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    def send_invite_mail(self):
        support_email_address = settings.SUPPORT_EMAIL
        rendered_templates = self.generate_invite_mail()

        send_mail(
            "Welcome to the Icebreaker One Constellation",
            rendered_templates["text"],
            support_email_address,
            [self.user.email],
            html_message=rendered_templates["html"],
        )

    def generate_invite_mail(self):
        support_email_address = settings.SUPPORT_EMAIL

        rendered_invite_txt = render_to_string(
            "invite_new_profile.txt",
            {"profile": self, "support_email_address": support_email_address},
        )
        rendered_invite_html = render_to_string(
            "invite_new_profile.mjml.html",
            {"profile": self, "support_email_address": support_email_address},
        )

        return {"text": rendered_invite_txt, "html": rendered_invite_html}
