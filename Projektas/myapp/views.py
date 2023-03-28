from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

def index(request):
    return render(request, "index.html", {})


def services(request):
    return render(request, "boxes.html", {})


def login(request):
    return render(request, "login.html", {})


def register(request):
    form = CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, "register.html", context)
