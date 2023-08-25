from django.urls import path

from .views import HomeView, HashRedirectView

urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("<str:hash_url>", HashRedirectView.as_view(), name="hash_redirect"),
]
