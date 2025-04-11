

import stripe
from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import Profile  #  On importe Profile


stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    # Vérifier si l'utilisateur est déjà premium
    if profile.is_premium:
        return Response({"message": "Tu es déjà premium !"}, status=400)

    # Récupérer le type d'abonnement demandé (mensuel ou annuel)
    data = request.data  # On récupère le choix de l'utilisateur depuis la requête
    plan_type = data.get("plan", "monthly")  #  Par défaut : mensuel

    # Sélectionner le `price_id` en fonction du choix
    if plan_type == "monthly":
        price_id = settings.STRIPE_PRICE_ID_MONTHLY
    elif plan_type == "yearly":
        price_id = settings.STRIPE_PRICE_ID_YEARLY
    else:
        return Response({"error": "Plan invalide"}, status=400)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price": price_id,  #  On utilise le bon price_id
                "quantity": 1,
            }],
            mode="subscription",
            success_url= "http://127.0.0.1:8000/payment-success/",
            cancel_url="http://127.0.0.1:8000/cancel/",
            customer_email=user.email,
        )

        print(f"✅ Session Stripe créée : {checkout_session.url}")  #  Debugging
        return Response({"checkout_url": checkout_session.url})

    except Exception as e:
        print(f"🚨 Erreur Stripe : {str(e)}")  #  Debugging
        return Response({"error": str(e)}, status=500)


def payment_success(request):
    return render(request, "payment_success.html")
