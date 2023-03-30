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
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        password2 = request.POST.get('pass2')

        if password == password2:
            if User.objects.filter(username=uname).exists():
                return HttpResponse('Error, vartotojo vardas uzimtas')
            else:
                if User.objects.filter(email=email).exists():
                    return HttpResponse('Error, el. pastas uzimtas')
                else:
                    new_user = User.objects.create_user(uname, email, password)
                    new_user.first_name = fname
                    new_user.last_name = lname

                    new_user.save()
                    messages.info(request, f"Vartotojas {uname} sukurtas")
                    return redirect('login')
        else:
            messages.error(request, "Slaptazodziai nesutampa")
            return redirect("register")
    return render(request, "register.html", {})


def loginas(request):
    if request.method == "POST":
        name = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('Error, user does not exist')

    return render(request, "login.html", {})


def logoutuser(request):
    logout(request)
    return redirect('index')
