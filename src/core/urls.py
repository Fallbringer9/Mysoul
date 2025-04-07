from django.urls import path
from django.views.generic import TemplateView

from core.views import dashboard, load_journal, load_challenges, show_challenge_form, add_challenge, delete_challenge, \
    edit_challenge, update_challenge

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("dashboard/", dashboard, name="dashboard"),  # ✅ Utilisation de la vraie view du dashboard
    path("profile/", TemplateView.as_view(template_name="profile.html"), name="profile"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),

    # HTMX
    path("load-journal/", load_journal, name="load_journal"),
    path("load-challenges/", load_challenges, name="load_challenges"),
    path("show-challenge-form/", show_challenge_form, name="show_challenge_form"),
    path("add-challenge/", add_challenge, name="add_challenge"),
    path("delete-challenge/<int:challenge_id>/", delete_challenge, name="delete_challenge"),
    path("edit-challenge/<int:challenge_id>/", edit_challenge, name="edit_challenge"),
    path("update-challenge/<int:challenge_id>/", update_challenge, name="update_challenge"),
]

