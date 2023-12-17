from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages.views import flatpage
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import RedirectView
from rest_framework.authtoken.views import obtain_auth_token

from cl8.admin import site as cl8_admin_site

from cl8.users.api.views import (
    ProfileCreateView,
    ProfileDetailView,
    ProfileVcardView,
    ProfileEditView,
    TagAutoCompleteView,
    homepage,
)


urlpatterns = [
    #
    # main profile functionality
    path("", homepage, name="home"),
    path("profiles/create/", ProfileCreateView.as_view(), name="profile-create"),
    path("profiles/<slug>.vcf", ProfileVcardView.as_view(), name="profile-vcard"),
    path("profiles/<slug>", ProfileDetailView.as_view(), name="profile-detail"),
    path("profiles/<slug>/edit", ProfileEditView.as_view(), name="profile-edit"),
    #
    # Django Admin, use {% url 'admin:index' %}
    # use this to sanity check differences between the default
    # and our custom one with the extra links
    # from django.contrib import admin
    # path("admin/", admin.site.urls),
    path("admin/", cl8_admin_site.urls),
    #
    # default allauth User management
    path("users/", include("cl8.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # add our extra custom providers and views for sign-in with slack
    path("accounts/", include("cl8.users.slack_openid_connect.urls")),
    # basic CMS pages
    path("about/", flatpage, {"url": "/about/"}, name="about"),
    path("privacy/", flatpage, {"url": "/privacy/"}, name="privacy"),
    #
    path(
        "favicon.ico", RedirectView.as_view(url="/static/images/favicons/favicon.ico")
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("", include("cl8.users.api.passwordless_urls")),
    path(
        "api/autocomplete/tags-read-only/",
        TagAutoCompleteView.as_view(),
        name="tag-autocomplete",
    ),
    # we have a second autocomplete view that allows users to create new tags
    # to use on the profile edit page
    path(
        "api/autocomplete/tags/",
        TagAutoCompleteView.as_view(
            create_field="name",
        ),
        name="tag-autocomplete-with-create",
    ),
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
        urlpatterns = [
            path("__reload__/", include("django_browser_reload.urls"))
        ] + urlpatterns

# Finally add the catch-all route for flat pages.
# The "(?!static/)" means that we don't want to match any url that
# starts with "static/", which is where our static files are served from.
urlpatterns += [
    re_path(r"^(?!static/)(?P<url>.*/)$", flatpage),
]
