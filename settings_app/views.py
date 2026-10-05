
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def settings_home(request):
    return render(request, "settings/home.html")