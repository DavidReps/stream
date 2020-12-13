from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.
#registration

def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST or None)

            if form.is_valid():
                user = form.save()

                #get raw password
                raw_password = form.cleaned_data.get('password1')

                #authenitcate user
                user = authenticate(username = user.username, password=raw_password)

                login(request, user)

                return redirect("main:home")

        else:
            form = RegistrationForm()
        return render(request, "accounts/register.html", {"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("main:home")

                else:
                    return render(request, 'accounts/login.html', {"error": "your account has ben disabled."})

            else:
                return render(request, 'accounts/login.html', {"error": "sorry chief, invalid username or password."})

        return render(request, 'accounts/login.html')

def logout_user(request):
    if request.user.is_authenticated:

        logout(request)
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")