from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.flatpages.views import flatpage
from cl8.users.admin import constellation_admin as cl8_admin
from cl8.users.views import sample_csv_template
from cl8.users.api.views import HomepageView

urlpatterns = [
    # serve the vue template instead of the default home
    path("", HomepageView.as_view(), name="home"),
    # Django Admin, use {% url 'admin:index' %}
    path("advanced-admin/", admin.site.urls),
    path(
        "admin/import-csv/sample.csv", sample_csv_template, name="sample-csv-template"
    ),
    # User management
    path("users/", include("cl8.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # add our extra custom providers and views for sign-in with slack
    path("accounts/", include("cl8.users.slacko.urls")),
    # basic CMS pages
    path("about/", flatpage, {"url": "/about/"}, name="about"),
    path("privacy/", flatpage, {"url": "/privacy/"}, name="privacy"),
    #
    path(
        "favicon.ico", RedirectView.as_view(url="/static/images/favicons/favicon.ico")
    ),
    path("admin/", cl8_admin.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("", include("cl8.users.api.passwordless_urls")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    if "django_browser_reload" in settings.INSTALLED_APPS:
        urlpatterns = [path("__reload__/", include("django_browser_reload.urls"))] + urlpatterns


