from django.conf import settings

from rest_framework.routers import DefaultRouter, SimpleRouter

from backend.users.api.views import (
    ProfileViewSet,
    TagViewSet,
    ClusterViewSet,
    ProfilePhotoUploadView,
)
from django.urls import path


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("profiles", ProfileViewSet)
router.register("clusters", ClusterViewSet)
router.register("tags", TagViewSet)

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("upload/<id>/", ProfilePhotoUploadView.as_view(), name="profile-pic-upload"),
]
