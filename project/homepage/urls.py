from django.urls import path

from .views import HomepageView, HomeView

app_name = "homepage"

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("home/", HomeView.as_view(), name="home"),
]
