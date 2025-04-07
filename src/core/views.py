from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from challenges.forms import ChallengeForm
from journal.models import JournalEntry
from challenges.models import Challenge

@login_required
def dashboard(request):
    user = request.user  # Récupère l'utilisateur connecté

    # Charger les défis et entrées du journal de l'utilisateur
    challenges = Challenge.objects.filter(user=user)  # Récupérer uniquement les défis de l'utilisateur
    entries = JournalEntry.objects.filter(user=user).order_by('-date')  # Filtrer aussi les entrées du journal

    # Statistiques dynamiques
    stats = {
        "challenges_count": challenges.count(),
        "total_time": sum(challenge.duration for challenge in challenges),  # Supposons qu'il y ait un champ "duration"
        "average_mood": entries.aggregate(Avg('mood'))['mood__avg'] if entries.exists() else 0,  # Moyenne de l'humeur
    }

    return render(request, "dashboard.html", {
        "user": user,
        "stats": stats,
        "challenges": challenges,
        "entries": entries,
    })

@login_required
def load_journal(request):
    """ Charger les entrées du journal de l'utilisateur connecté """
    entries = JournalEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, "partials/journal_entries.html", {"entries": entries})

@login_required
def load_challenges(request):
    """ Charger les défis de l'utilisateur connecté """
    challenges = Challenge.objects.filter(user=request.user)
    return render(request, "partials/challenges.html", {"challenges": challenges})

@login_required
def show_challenge_form(request):
    """ Affiche le formulaire de création d’un défi """
    form = ChallengeForm()
    return render(request, "partials/challenge_form.html", {"form": form})

@login_required
def add_challenge(request):
    """ Ajoute un défi et met à jour la liste des défis """
    if request.method == "POST":
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.user = request.user  # Associer le défi à l'utilisateur
            challenge.save()

    # Retourner la liste mise à jour
    challenges = Challenge.objects.filter(user=request.user)
    return render(request, "partials/challenges.html", {"challenges": challenges})


@login_required
def delete_challenge(request, challenge_id):
    """ Supprime un défi si la méthode est DELETE ou si _method=DELETE est envoyé en POST """
    if request.method == "DELETE" or request.POST.get("_method") == "DELETE":
        challenge = get_object_or_404(Challenge, id=challenge_id, user=request.user)
        challenge.delete()
        return JsonResponse({"message": "Défi supprimé"}, status=200)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


@login_required
def edit_challenge(request, challenge_id):
    """ Affiche le formulaire de modification d’un défi """
    challenge = get_object_or_404(Challenge, id=challenge_id, user=request.user)
    form = ChallengeForm(instance=challenge)
    return render(request, "partials/challenge_edit_form.html", {"form": form, "challenge": challenge})

@login_required
def update_challenge(request, challenge_id):
    """ Met à jour un défi et recharge la liste """
    challenge = get_object_or_404(Challenge, id=challenge_id, user=request.user)

    if request.method == "POST":
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()

    # Retourner la liste mise à jour
    challenges = Challenge.objects.filter(user=request.user)
    return render(request, "partials/challenges.html", {"challenges": challenges})


