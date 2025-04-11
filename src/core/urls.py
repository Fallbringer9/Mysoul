from django.urls import path
from django.views.generic import TemplateView

from core.views import dashboard, load_journal, load_challenges, show_challenge_form, add_challenge, delete_challenge, \
    edit_challenge, update_challenge, profile_view, edit_profile, deactivate_account, confirm_deactivate_account_view
from payments.views import payment_success

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("dashboard/", dashboard, name="dashboard"),  # ✅ Utilisation de la vraie view du dashboard
    path("profile/", profile_view, name="profile"),
    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register"),
    path("payment-success/", payment_success, name="payment_success"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/deactivate/", deactivate_account, name="deactivate_account"),
    path("profile/deactivate/", confirm_deactivate_account_view, name="deactivate_account"),
    path("profile/deactivate/confirm/", deactivate_account, name="confirm_deactivate_account"),




    # HTMX
    path("load-journal/", load_journal, name="load_journal"),
    path("load-challenges/", load_challenges, name="load_challenges"),
    path("show-challenge-form/", show_challenge_form, name="show_challenge_form"),
    path("add-challenge/", add_challenge, name="add_challenge"),
    path("delete-challenge/<int:challenge_id>/", delete_challenge, name="delete_challenge"),
    path("edit-challenge/<int:challenge_id>/", edit_challenge, name="edit_challenge"),
    path("update-challenge/<int:challenge_id>/", update_challenge, name="update_challenge"),
]

