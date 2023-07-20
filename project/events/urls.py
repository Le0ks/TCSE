from django.urls import path

from .views import (
    CreateEventView,
    CategoryDetailView,
    EventListView,
    CreateTestView,
    EventDetailView,
    EventRegistrationView,
    TestTaskDetailView,
    EventResultView,
    EventRatingView,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="events_list"),
    path("create/", CreateEventView.as_view(), name="create_event"),
    path("create/testwork", CreateTestView.as_view(), name="create_test"),
    path("<slug:category_name>/", CategoryDetailView.as_view(), name="category_detail"),
    path(
        "<slug:category_name>/<slug:event_name>/",
        EventDetailView.as_view(),
        name="event_detail",
    ),
    path(
        "<slug:category_name>/<slug:event_name>/registration/",
        EventRegistrationView.as_view(),
        name="event_registration",
    ),
    path(
        "testwork/<slug:event_name>/<int:number_of_task>/",
        TestTaskDetailView.as_view(),
        name="event_testwork_task",
    ),
    path(
        "<slug:category_name>/<slug:event_name>/result/",
        EventResultView.as_view(),
        name="event_result",
    ),
    path(
        "<slug:category_name>/<slug:event_name>/rating/",
        EventRatingView.as_view(),
        name="event_rating",
    ),
]
