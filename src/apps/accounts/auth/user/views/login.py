from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from apps.accounts.auth.user.forms import SignUpForm, LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


