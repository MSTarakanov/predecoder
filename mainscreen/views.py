from django.shortcuts import render, redirect
from .forms import EmailForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from x86.models import IntelDescription
# Create your views here.

def index(request):
    print(request.user)
    form = UserRegistrationForm()
    user = None
    if request.method == "POST":
        if 'login' in request.POST:
            form = UserRegistrationForm(request.POST)
            email = str(request.POST['email']).split('@', 1)
            username = email[0]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                print('no user')
            if user is None:
                users_dict = dict(username=username, password='')
                user = User.objects.create(**users_dict)
                user.save()
                users_intel_desc = IntelDescription.objects.create(user=user)

            print(user)
            login(request, user)
        elif 'logout' in request.POST:
            logout(request)

    return render(request, 'mainscreen/main.html', {'form': form})

