from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Mysoul import settings
from accounts.views import AdminChallengeViewSet, UserProfileView, PremiumChallengeViewSet
from api.views import stripe_webhook
from journal.views import AdvancedStatsView, JournalEntryViewSet
from payments.views import create_checkout_session
from challenges.views import ChallengeViewSet, FreeChallengeViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import delete_challenge


# DRF Router
router = DefaultRouter()
router.register('entries', JournalEntryViewSet, 'journalentry')
router.register('admin-challenges', AdminChallengeViewSet, basename='admin-challenges')
router.register('challenges', ChallengeViewSet, basename='challenge')
router.register('premium-challenges', PremiumChallengeViewSet, basename='premium-challenges')
router.register('free-challenges', FreeChallengeViewSet, basename='free-challenges')

# Endpoints API uniquement
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('accounts/', include('accounts.urls')),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('reactivate/', UserProfileView.as_view(), name='reactivate'),
    path('stats/advanced/', AdvancedStatsView.as_view(), name='advanced-stats'),
    path('challenges/delete/<int:challenge_id>/', delete_challenge, name='delete_challenge'),


    # Paiements avec Stripe
    path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),
    path("stripe/webhooks/", stripe_webhook, name="stripe-webhook"),
    path("stripe/create-checkout-session/", create_checkout_session, name="create-checkout-session"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
