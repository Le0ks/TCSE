from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import settings


urlpatterns = [
    path("", include("homepage.urls")),
    path("events/", include("events.urls")),
    path("admin/", admin.site.urls),
    path("about/", include("about.urls")),
    path("", include("users.urls")),
    path("feedback/", include("feedback.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__", include(debug_toolbar.urls)),)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
