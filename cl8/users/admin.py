from django.contrib import admin, messages
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from taggit.forms import TagField
from taggit.models import Tag
from taggit_labels.widgets import LabelWidget

# from .site_admin import constellation_admin
from cl8.users.forms import UserChangeForm, UserCreationForm
from cl8.users.models import Cluster, Constellation, Profile

User = get_user_model()


class ProfileAdminForm(ModelForm):
    tags = TagField(required=False, widget=LabelWidget)
    # clusters = TagField(
    #     required=False,
    #     widget=LabelWidget(model=Cluster),
    #     help_text="Clusters the user wants to be included in",
    # )


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    # add_form = UserCreationForm
    # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    readonly_fields = ["last_login", "date_joined"]

    # def get_fieldsets(self, request, *args, **kwargs):
    #     if request.user.is_superuser:
    #         return (
    #             (None, {"fields": ("username", "password")}),
    #             (
    #                 "Personal info",
    #                 {
    #                     "fields": (
    #                         "name",
    #                         "email",
    #                     )
    #                 },
    #             ),
    #             (
    #                 "Permissions",
    #                 {
    #                     "fields": (
    #                         "is_active",
    #                         "is_staff",
    #                         "is_superuser",
    #                         "groups",
    #                         "user_permissions",
    #                     ),
    #                 },
    #             ),
    #             ("Important dates", {"fields": ("last_login", "date_joined")}),
    #         )

    #     return (
    #         (None, {"fields": ("username", "password")}),
    #         (
    #             "Personal info",
    #             {
    #                 "fields": (
    #                     "name",
    #                     "email",
    #                 )
    #             },
    #         ),
    #         ("Important dates", {"fields": ("last_login", "date_joined")}),
    #     )


# @admin.register(Profile, site=constellation_admin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ["name", "email", "visible"]
    search_fields = ["user__name", "user__email", "tags__name"]
    actions = ["make_visible", "make_invisible", "send_invite_mail"]

    def has_set_visibility_permission(self, request):
        opts = self.opts
        codename = "set_visibility"
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def has_send_invite_mail_permission(self, request):
        opts = self.opts
        codename = "send_invite_email"
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    @admin.action(
        permissions=["set_visibility"],
        description="Make visible",
    )
    def make_visible(self, request, queryset):
        queryset.update(visible=True)

    @admin.action(
        permissions=["set_visibility"],
        description="Make invisible",
    )
    def make_invisible(self, request, queryset):
        queryset.update(visible=False)

    @admin.action(
        permissions=["send_invite_mail"],
        description="Send invite email",
    )
    def send_invite_mail(self, request, queryset):
        sent_emails = []
        for profile in queryset:
            result = profile.send_invite_mail()
            sent_emails.append(result)

        self.message_user(
            request,
            ngettext(
                "%d invite successfully sent.",
                "%d invites successfully sent.",
                len(sent_emails),
            )
            % len(sent_emails),
            messages.SUCCESS,
        )


@admin.register(Constellation)
class ConstellationAdmin(admin.ModelAdmin):
    class Meta:
        model = Constellation


# make the default Tag model available to admins to change
# constellation_admin.register(Tag)
