from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
import csv
from django.http import HttpResponse


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def sample_csv_template(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="sample.csv"'

    sampleProfile = {
        "name": "Example name",
        "admin": False,
        "visible": False,
        "tags": "comma, separated tags, here in quotes",
        "photo": "https://link.website.com/profile-photo.jpg",
        "email": "email@example.com",
        "phone": "07974 123 456",
        "website": "https://example.com",
        "twitter": "https://twitter.com/username",
        "linkedin": "https://linkedin.com/username",
        "facebook": "https://facebook.com/username",
        "bio": "A paragraph of text. Will be rendered as markdown and can contain links.",
    }

    writer = csv.writer(response)
    writer.writerow(sampleProfile.keys())
    writer.writerow(sampleProfile.values())

    return response
