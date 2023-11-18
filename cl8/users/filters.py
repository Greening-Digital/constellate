import django_filters
from cl8.users import models as cl8_models
from taggit import models as taggit_models
from dal import autocomplete

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class ProfileFilter(django_filters.FilterSet):
    bio = django_filters.CharFilter(method="search_fulltext")

    # We now hide the select2 widget in the profile filter component shown to users
    # but keeping this helps for debugging tag filtering issues
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags",
        label="Tags",
        queryset=taggit_models.Tag.objects.all(),
        # comment these out, and remove the hidden class
        # on the profile filter template to use the select2 autocomplete
        # widget
        # widget=autocomplete.ModelSelect2Multiple(url="tag-autocomplete"),
        # conjoined means that all tags must be present, not just any of the tags
        conjoined=True,
    )

    def search_fulltext(self, queryset, field_name, value):
        """
        Override the default search behaviour to use Postgres full text search, to search
        a number of fields simultaneously, returning a ranked listing of results
        """
        # https://github.com/carltongibson/django-filter/issues/1039
        # https://stackoverflow.com/questions/76397037/django-full-text-search-taggit

        search_query = SearchQuery(value, search_type="websearch")
        search_vector = SearchVector(
            # we want the user's name to be searchable
            "user__name",
            # along with all the text of their bio
            "user__email",
            "bio",
            # and location
            "location",
            # and the text of all the tags associated with the profile
            "tags__name",
            # and any social media handles
            "twitter",
            "linkedin",
            "facebook",
            "website",
            "organisation",
        )

        return (
            # this ranks our results by how well they match the search query
            # annotating each result with a score in the property 'rank' from 0 to 1
            queryset.annotate(rank=SearchRank(search_vector, search_query))
            .filter(rank__gt=0)
            .distinct()
            .order_by("-rank")
        )

    class Meta:
        model = cl8_models.Profile
        fields = ["bio"]
