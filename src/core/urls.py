from django.urls import path
from django.views.generic import TemplateView
from core.views import load_journal, load_challenges

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
    path("profile/", TemplateView.as_view(template_name="profile.html"), name="profile"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),

    # HTMX
    path("load-journal/", load_journal, name="load_journal"),
    path("load-challenges/", load_challenges, name="load_challenges"),
]
