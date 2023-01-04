import django_filters
from cl8.users import models as cl8_models
from taggit import models as taggit_models
from dal import autocomplete


class ProfileFilter(django_filters.FilterSet):
    bio = django_filters.CharFilter(lookup_expr='icontains')

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags",
        label="Tags",
        queryset=taggit_models.Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url="tag-autocomplete"),
        conjoined=True
    )

    class Meta:
        model = cl8_models.Profile
        fields = ['bio']
