from django.urls import path

from .views import (
    CreateEventListView,
    CreateMixedWorkView,
    CreateTestView,
    CreateWrittenWorkView,
    EventConnectView,
    EventDetailView,
    EventListView,
    EventRatingView,
    EventRegistrationView,
    EventResultView,
    MixedWorkTasksDetailView,
    TestTasksDetailView,
    WrittenWorkTasksDetailView,
)


app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="list_of_events"),
    path("create/", CreateEventListView.as_view(), name="create_event"),
    path("create/testwork/", CreateTestView.as_view(), name="create_test"),
    path(
        "create/written_work/",
        EventListView.as_view(),
        name="create_written_work",
    ),
    path(
        "create/mixed_work/",
        EventListView.as_view(),
        name="create_mixed_work",
    ),
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
        TestTasksDetailView.as_view(),
        name="event_testwork_task",
    ),
    path(
        "writtten_work/<slug:event_name>/<int:number_of_task>",
        EventListView.as_view(),
        name="event_written_work_task",
    ),
    path(
        "mixed_work/<slug:event_name>/<int:number_of_task>",
        EventListView.as_view(),
        name="event_mixed_work_task",
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
    path("connect/", EventConnectView.as_view(), name="event_connect"),
]
