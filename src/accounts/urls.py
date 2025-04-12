from django.urls import path
from .views import PasswordResetView, PasswordResetConfirmView, UserRegisterView

urlpatterns = [
    path('reset-password/', PasswordResetView.as_view(), name='password-reset'),
    path('reset-password/<int:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('register/', UserRegisterView.as_view(), name='api-register')

]
