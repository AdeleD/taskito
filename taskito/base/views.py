from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse


def home(request):
    return HttpResponseRedirect(reverse('alltasks'))


def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('alltasks'))
        messages.error(request, 'Le login ou le mot de passe est invalide')
    return render(request, 'login.html')


@login_required
def log_out(request):
    logout(request)
    return render(request, 'login.html')
