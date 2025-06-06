
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')



def access_denied(request):
    return render(request, 'access_denied.html', status=403)
