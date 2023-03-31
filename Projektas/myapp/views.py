from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages


def index(request):
    return render(request, "index.html", {})


def services(request):
    return render(request, "services.html", {})


def register(request):
    uname = request.POST.get('uname')
    nickname = User.objects.filter(username=uname).exists()
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        password2 = request.POST.get('pass2')
        nickname = User.objects.filter(username=uname).exists()

        if password == password2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, f"Slapyvardis '{uname}' užimtas!")
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"El.paštas '{email}' užimtas!")
                    return redirect("register")
                else:
                    new_user = User.objects.create_user(uname, email, password)
                    new_user.save()
                    return redirect('login')
        else:
            messages.error(request, "Slaptažodžiai nesutampa!")
            return redirect("register")
    return render(request, "register.html", {"nickname": nickname})


def loginas(request):
    if request.method == "POST":
        name = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Vartotojas neegzistuoja arba neteisingi duomenys!")
            return redirect('login')

    return render(request, "login.html", {})


def logoutuser(request):
    logout(request)
    return redirect('index')
