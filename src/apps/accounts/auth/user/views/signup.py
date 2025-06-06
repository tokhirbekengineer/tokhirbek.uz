# apps/accounts/auth/user/views.py (yoki sizning views.py faylingiz)
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from apps.accounts.auth.user.forms import SignUpForm  # yoki to‘g‘ri yo‘l bilan import qiling

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Foydalanuvchini saqlaymiz
            form.save()

            # Foydalanuvchini authenticate qilamiz (backendni aniqlash uchun)
            username_or_email = form.cleaned_data.get('username_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)  # Foydalanuvchini tizimga kiritamiz
                return redirect('home')  # Kerakli sahifaga yo'naltirish
            else:
                # Agar authenticate bo‘lmasa, xatolik berish mumkin
                form.add_error(None, 'Tizimga kirishda muammo yuz berdi. Iltimos, qaytadan urinib ko‘ring.')
    else:
        form = SignUpForm()

    return render(request, 'auth/signup.html', {'form': form})
