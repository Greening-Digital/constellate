from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget


from .site_admin import constellation_admin
from backend.users.forms import UserChangeForm, UserCreationForm
from backend.users.models import Profile, Cluster

User = get_user_model()


class ProfileAdminForm(ModelForm):
    # tags = TagField(required=False, widget=LabelWidget)
    clusters = TagField(
        required=False,
        widget=LabelWidget(model=Cluster),
        help_text="Clusters the user wants to be included in",
    )


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(Profile, site=constellation_admin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm


@admin.register(Cluster)
@admin.register(Cluster, site=constellation_admin)
class ClusterAdmin(admin.ModelAdmin):
    pass
