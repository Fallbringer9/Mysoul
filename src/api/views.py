
import stripe
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework import viewsets
from Mysoul import settings
from accounts.models import Profile
from journal.models import JournalEntry
from journal.serializers import JournalEntrySerializers

class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializers

logger = logging.getLogger("mysoul")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        logger.info("Webhook Stripe bien reçu !")

    except ValueError as e:
        logger.error(f"Erreur de payload : {e}")
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Signature invalide : {e}")
        return HttpResponse(status=400)

    #  Paiement réussi (abonnement ou renouvellement)
    if event["type"] == "invoice.paid":
        session = event["data"]["object"]
        stripe_customer_id = session.get("customer")  # ID unique Stripe du client

        if stripe_customer_id:
            try:
                profile = Profile.objects.get(stripe_customer_id=stripe_customer_id)
                profile.activate_premium(30)  #  Utilisation de ta méthode
                logger.info(f"Renouvellement réussi pour {profile.user.email}")

                return JsonResponse({"message": "Renouvellement d'abonnement mis à jour"}, status=200)

            except Profile.DoesNotExist:
                logger.error(f"Utilisateur introuvable avec stripe_customer_id {stripe_customer_id}")
                return JsonResponse({"error": "Utilisateur introuvable"}, status=404)

    #  Annulation d'abonnement
    elif event["type"] == "customer.subscription.deleted":
        session = event["data"]["object"]
        stripe_customer_id = session.get("customer")

        if stripe_customer_id:
            try:
                profile = Profile.objects.get(stripe_customer_id=stripe_customer_id)

                #  Option : Laisser Premium actif jusqu'à expiration
                logger.info(
                    f"Abonnement annulé pour {profile.user.email}, premium actif jusqu'au {profile.premium_expiration_date}")

                return JsonResponse({"message": "Abonnement annulé, premium actif jusqu'à expiration"}, status=200)

            except Profile.DoesNotExist:
                logger.error(f"Utilisateur introuvable avec stripe_customer_id {stripe_customer_id}")
                return JsonResponse({"error": "Utilisateur introuvable"}, status=404)

    return HttpResponse(status=200)

class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "core/payment_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)

        context["is_premium"] = profile.is_premium
        context["premium_expiration_date"] = profile.premium_expiration_date
        return context


