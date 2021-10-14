from django.shortcuts import render, redirect
from .forms import EmailForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from x86.models import IntelDescription
from mips.models import MipsDescription
# Create your views here.

def is_valid_mail(email_domen):
    if email_domen == 'edu.hse.ru':
        return True
    return False

def index(request):
    print(request.user)
    form = UserRegistrationForm()
    user = None
    error_massage = None

    if request.method == "POST":
        if 'login' in request.POST:
            form = UserRegistrationForm(request.POST)
            email = str(request.POST['email']).split('@', 1)
            if not is_valid_mail(email[1]):
                error_massage = "Введите верный email с @edu.hse.ru"
                return render(request, 'mainscreen/main.html', {'form': form, 'error_massage': error_massage})
            username = email[0]
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                print('no user')
            if user is None:
                users_dict = dict(username=username, password='')
                user = User.objects.create(**users_dict)
                user.save()
                IntelDescription.objects.create(user=user)
                MipsDescription.objects.create(user=user)

            print(user)
            login(request, user)
        elif 'logout' in request.POST:
            logout(request)

    return render(request, 'mainscreen/main.html', {'form': form, 'error_massage': error_massage})

