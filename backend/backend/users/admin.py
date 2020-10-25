from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget
from taggit.models import Tag

from .site_admin import constellation_admin
from backend.users.forms import UserChangeForm, UserCreationForm
from backend.users.models import Profile, Cluster
from django.utils.safestring import mark_safe

User = get_user_model()


class ProfileAdminForm(ModelForm):
    # tags = TagField(required=False, widget=LabelWidget)
    clusters = TagField(
        required=False,
        widget=LabelWidget(model=Cluster),
        help_text="Clusters the user wants to be included in",
    )


@admin.register(User)
@admin.register(User, site=constellation_admin)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    readonly_fields = ["last_login", "date_joined"]

    def get_fieldsets(self, request, *args, **kwargs):

        if request.user.is_superuser:
            return (
                (None, {"fields": ("username", "password")}),
                ("Personal info", {"fields": ("email",)}),
                (
                    "Permissions",
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                            "is_superuser",
                            "groups",
                            "user_permissions",
                        ),
                    },
                ),
                ("Important dates", {"fields": ("last_login", "date_joined")}),
            )

        return (
            (None, {"fields": ("username", "password")}),
            ("Personal info", {"fields": ("email",)}),
            ("Important dates", {"fields": ("last_login", "date_joined")}),
        )


@admin.register(Profile, site=constellation_admin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm


@admin.register(Cluster)
@admin.register(Cluster, site=constellation_admin)
class ClusterAdmin(admin.ModelAdmin):
    pass


# make the default Tag model available to admins to change
constellation_admin.register(Tag)
