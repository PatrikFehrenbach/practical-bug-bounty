from django.shortcuts import render
from .models import ChallengePlatform
# Create your views here.
def challenges(request):
    all_challenges = ChallengePlatform.objects.filter(is_active=True)
    return render(request, 'challenges.html', {'challenges': all_challenges})
