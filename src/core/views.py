from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from accounts.models import Profile
from challenges.forms import ChallengeForm
from journal.forms import JournalEntryForm
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

@login_required
def profile_view(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    return render(request, "profile.html", {
        "user": user,
        "profile": profile
    })


@login_required
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        email = request.POST.get("email")
        avatar = request.FILES.get("avatar")

        if email:
            request.user.email = email
            request.user.save()

        if avatar:
            profile.avatar = avatar
            profile.save()

        return redirect("profile")

    return render(request, "profile_edit.html", {
        "user": request.user,
        "profile": profile
    })

@require_http_methods(["POST"])
@login_required
def deactivate_account(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect("login")

@login_required
@require_http_methods(["GET"])
def confirm_deactivate_account_view(request):
    return render(request, "confirm_deactivation.html")

@login_required
@require_http_methods(["POST"])
def deactivate_account(request):
    user = request.user
    user.is_active = False
    user.save()
    return redirect("login")

@login_required
def journal_view(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, "journal.html", {"entries": entries})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next") or "dashboard"
            return redirect(next_url)
        else:
            messages.error(request, "Identifiants invalides")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('home')



@login_required
def journal_view(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('journal')
    else:
        form = JournalEntryForm()

    return render(request, "journal.html", {
        "entries": entries,
        "form": form,
    })

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "register.html")

        user = User.objects.create_user(username=username, email=email, password=password)

        # 👉 FORCEMENT du backend car Django a plusieurs backends
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        next_url = request.GET.get("next") or "dashboard"
        return redirect(next_url)

    return render(request, "register.html")
