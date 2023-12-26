from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from events.views import CategoryDetailView, CategoryListView

from . import settings
from . import views

urlpatterns = [
    path("", include("homepage.urls")),
    path("events/", include("events.urls")),
    path("admin/", admin.site.urls),
    path("about/", include("about.urls")),
    path("categories/", CategoryListView.as_view(), name="list_of_category"),
    path(
        "categories/<slug:category_name>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("", include("users.urls")),
    path("feedback/", include("feedback.urls")),
    path(
        "social-auth/",
        include("social_django.urls", namespace="social_auth"),
    ),
]

handler404 = views.custom_404
handler500 = views.custom_500

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__", include(debug_toolbar.urls)),)

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
