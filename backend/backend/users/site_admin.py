from io import StringIO
from django.contrib.admin.sites import AdminSite
from django import forms
from django.urls import path
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .importers import ProfileImporter


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ConstellationAdmin(AdminSite):
    # This is a standard authentication form that allows non-staff users
    # login_form = AuthenticationForm
    site_header = "Constellate Admin"
    index_title = "Constellate Admin"

    def get_urls(self):
        urls = super().get_urls()
        patterns = [
            path("import-csv/", self.import_csv, name="import-profiles"),
        ]

        return patterns + urls

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        patterns = [
            {
                "name": "Utilities",
                "app_label": "backend",
                "app_url": "/admin/import-csv/",
                "models": [
                    {
                        "name": "Profile Import",
                        "object_name": "profile_import",
                        "admin_url": "/admin/import-csv/",
                        "view_only": True,
                    }
                ],
            }
        ]
        return app_list + patterns

    def import_csv(self, request):
        from .admin import ProfileAdmin

        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            # the uploaded file is bytestream,
            # but we need a string
            csv_text_file = StringIO(csv_file.read().decode("utf-8"))

            importer = ProfileImporter()
            importer.load_csv(csv_text_file)
            created_users = importer.create_users()

            messages.add_message(
                request,
                messages.INFO,
                f"Your csv file with users has been imported. {len(created_users)} new profiles were imported.",
            )

            return redirect("/admin/users/profile/")

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "profile_csv_import.html", payload)


constellation_admin = ConstellationAdmin(name="constellation_admin")
