from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Profile
from django import forms
from dal import autocomplete
from taggit import models as taggit_models
from django.forms import ModelMultipleChoiceField

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
    )

    class Meta:
        model = Profile
        fields = [
            "photo",
            "name",
            "location",
            "organisation",
            # "user_email",
            "bio",
            "tags",
            "twitter",
            "linkedin",
            "facebook",
            "visible",
        ]
