from dal import autocomplete
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _
from taggit import models as taggit_models

from .importers import safe_username
from .models import Profile

User = get_user_model()


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(auth_forms.UserCreationForm):
    error_message = auth_forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField()
    # email = forms.EmailField()

    tags = ModelMultipleChoiceField(
        queryset=taggit_models.Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url="tag-autocomplete-with-create"),
        required=False,
    )

    def save(self, commit=True):
        """ """
        self.instance.user.name = self.cleaned_data.get("name")
        self.instance.user.save()

        return super().save(commit=commit)

    class Meta:
        model = Profile
        fields = [
            "photo",
            "name",
            "phone",
            "location",
            "organisation",
            "bio",
            "tags",
            "twitter",
            "linkedin",
            "facebook",
            "visible",
        ]


class ProfileCreateForm(forms.ModelForm):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    tags = ModelMultipleChoiceField(
        queryset=taggit_models.Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url="tag-autocomplete-with-create"),
    )

    def save(self, commit=True):
        """
        Create a user, then save the corresponding profile object
        """

        email = self.cleaned_data.get("email")
        user, created = User.objects.get_or_create(
            email=email,
        )
        user.username = safe_username()
        user.name = self.cleaned_data.get("name")
        user.save()
        profile = Profile.objects.create(user=user)

        profile.phone = self.cleaned_data.get("phone")
        profile.website = self.cleaned_data.get("website")
        profile.twitter = self.cleaned_data.get("twitter")
        profile.facebook = self.cleaned_data.get("facebook")
        profile.linkedin = self.cleaned_data.get("linkedin")
        profile.bio = self.cleaned_data.get("bio")
        profile.visible = self.cleaned_data.get("visible")
        profile.short_id = safe_username()
        profile.import_id = "profile-form"
        profile.photo = self.cleaned_data.get("photo")

        profile.save()
        profile.update_thumbnail_urls()

        self.instance = profile
        result = super().save(commit=commit)

        # add the user to the 'member' group
        member_group = Group.objects.get(name="member")
        member_group.user_set.add(user)
        member_group.save()

        return result

    class Meta:
        model = Profile
        fields = [
            "photo",
            "name",
            "email",
            "location",
            "organisation",
            "bio",
            "phone",
            "tags",
            "twitter",
            "linkedin",
            "facebook",
            "visible",
        ]
