from django.shortcuts import render
from journal.models import JournalEntry
from challenges.models import Challenge

def load_journal(request):
    entries = JournalEntry.objects.all().order_by('-date')
    return render(request, "partials/journal_entries.html", {"entries": entries})

def load_challenges(request):
    challenges = Challenge.objects.all()
    return render(request, "partials/challenges.html", {"challenges": challenges})
