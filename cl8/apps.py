from django.contrib.admin.apps import AdminConfig


class Cl8AdminConfig(AdminConfig):
    default_site = "cl8.admin.ConstellationAdminSite"
