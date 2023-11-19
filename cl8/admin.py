import csv
import json
from io import StringIO

import allauth
import django
import rest_framework
import taggit
from django import forms
from django.contrib import messages
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path, reverse

from cl8.users.importers import CSVImporter, FireBaseImporter
from cl8.users.models import Constellation, Profile, User

from .users.admin import ConstellationAdmin, ProfileAdmin, UserAdmin

import logging

logger = logging.getLogger(__name__)


class CsvImportForm(forms.Form):
    import_file = forms.FileField()
    import_photos = forms.BooleanField(
        required=False,
        help_text="Import photos for each profile? (This can take a long time)",
    )

    def save(self):
        importer = CSVImporter()

        # we need to decode the uploaded file from bytes to string
        csv_file = StringIO(self.cleaned_data["import_file"].read().decode("utf-8"))

        importer.load_csv(csv_file)
        return importer.create_users(import_photos=self.cleaned_data["import_photos"])


class FirebaseImportForm(forms.Form):
    firebase_json = forms.FileField()
    import_photos = forms.BooleanField(
        required=False,
        help_text="Import photos for each profile? (This can take a long time)",
    )

    def save(self):
        try:
            importer = FireBaseImporter()
            breakpoint()
            json_content = self.cleaned_data["firebase_json"].read().decode("utf-8")

            parsed_data = json.loads(json_content)
            profiles = [prof for prof in parsed_data["userlist"].values()]
            return importer.add_users_from_json(
                profiles, import_photos=self.cleaned_data["import_photos"]
            )
        except Exception as ex:
            raise forms.ValidationError(
                "There was a problem importing your file. "
                "Please check it is a valid json file."
            )
            logger.exception(ex)


class ConstellationAdminSite(AdminSite):
    site_header = "Constellate Admin"
    site_title = "Constellate Admin Portal"
    index_title = "Constellate Admin"

    def get_urls(self):
        """
        Return the usual screens associated with registered models,
        plus the extra urls used for non-model oriented admin pages,
        """
        urls = super().get_urls()
        extra_urls = [
            path(
                "import-csv",
                self.admin_view(self.import_csv),
                name="import-profiles-from-csv",
            ),
            path(
                "profile-import-csv-template",
                self.admin_view(self.profile_import_csv_template),
                name="profile-import-csv-template",
            ),
            path(
                "import-firebase",
                self.admin_view(self.import_from_firebase),
                name="import-profiles-from-firebase",
            ),
        ]
        # order is important here. the default django admin
        # has a final_catch_all_view that will swallow anything
        # matching admin/<ANYTHING>, which means it will be
        # matched first, and any extra urls will not be matched.
        return extra_urls + urls

    def get_app_list(self, request):
        """
        Add the links to the extra screens on the admin index
        page, for importers and so on.
        """
        app_list = super().get_app_list(request)

        patterns = [
            {
                "name": "Utilities",
                "app_label": "cl8",
                "models": [
                    {
                        "name": "Profile Import",
                        "object_name": "profile_import",
                        "admin_url": reverse("admin:import-profiles-from-csv"),
                        "view_only": True,
                    },
                    {
                        "name": "Firebase Import",
                        "object_name": "firebase_import",
                        "admin_url": reverse("admin:import-profiles-from-firebase"),
                        "view_only": True,
                    },
                ],
            }
        ]
        return app_list + patterns

    def import_from_firebase(self, request):
        if not request.user.has_perm("profiles.import_profiles"):
            raise PermissionDenied

        if request.method == "POST":
            form = FirebaseImportForm(request.POST, request.FILES)
            if form.is_valid():
                created_users = form.save()

                messages.add_message(
                    request,
                    messages.INFO,
                    (
                        "Your json file with users has been imported. "
                        f"{len(created_users)} new profiles were imported.",
                    ),
                )

                return redirect("/admin/users/profile/")

        form = FirebaseImportForm()
        context = {**self.each_context(request), "form": form}
        return render(request, "profile_firebase_import.html", context)

    def import_csv(self, request):
        if not request.user.has_perm("profiles.import_profiles"):
            raise PermissionDenied

        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                created_users = form.save()

                messages.add_message(
                    request,
                    messages.INFO,
                    (
                        "Your csv file with users has been imported. "
                        f"{len(created_users)} new profiles were imported.",
                    ),
                )

                return redirect("/admin/users/profile/")

        form = CsvImportForm()

        context = {**self.each_context(request), "form": form}
        return render(request, "profile_csv_import.html", context)

    def profile_import_csv_template(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="sample.csv"'

        sampleProfile = {
            "name": "Example name",
            "admin": False,
            "visible": False,
            "tags": "comma, separated tags, 'here in quotes'",
            "photo": "https://link.website.com/profile-photo.jpg",
            "email": "email@example.com",
            "phone": "07974 123 456",
            "website": "https://example.com",
            "twitter": "https://twitter.com/username",
            "linkedin": "https://linkedin.com/username",
            "facebook": "https://facebook.com/username",
            "bio": "A paragraph of text. Will be rendered as markdown and can contain links.",
        }

        writer = csv.writer(response)
        writer.writerow(sampleProfile.keys())
        writer.writerow(sampleProfile.values())

        return response


site = ConstellationAdminSite()

# TODO: why does this not work?
# autodiscover_modules("admin", register_to=site)

# we list all the models brought via libraries their full paths
# to make it easier to see where they come, from in one place

# allauth
# used for tracking email addresses
# and for social logins via slack
site.register(
    allauth.socialaccount.models.SocialAccount,
    allauth.socialaccount.admin.SocialAccountAdmin,
)
site.register(
    allauth.socialaccount.models.SocialApp, allauth.socialaccount.admin.SocialAppAdmin
)
site.register(
    allauth.socialaccount.models.SocialToken,
    allauth.socialaccount.admin.SocialTokenAdmin,
)
site.register(
    allauth.account.models.EmailAddress,
    allauth.account.admin.EmailAddressAdmin,
)

# Used by DRF for token access when hitting the API
# TODO: given we no longer use Vue and the APIs it consumes should
# we remove all the API stuff?
site.register(
    rest_framework.authtoken.models.Token, rest_framework.authtoken.admin.TokenAdmin
)
site.register(django.contrib.sites.models.Site, django.contrib.sites.admin.SiteAdmin)
site.register(django.contrib.auth.models.Group, django.contrib.auth.admin.GroupAdmin)
site.register(
    django.contrib.flatpages.models.FlatPage,
    django.contrib.flatpages.admin.FlatPageAdmin,
)

# Used for tags
site.register(taggit.models.Tag, taggit.admin.TagAdmin)


site.register(Constellation, ConstellationAdmin)
site.register(Profile, ProfileAdmin)
site.register(User, UserAdmin)
