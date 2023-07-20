from django.urls import path

from .views import index


app_name = "feedback"

urlpatterns = [
    path("", index, name="feedback"),
]
