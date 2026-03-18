from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


def index(request):
    return redirect('login')


def signUp(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "The account was created successfully! Please login.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'signup.html', {'form': form})


def loginV(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        u = authenticate(request, username=username, password=password)

        if u is not None:
            login(request, u)
            return redirect('movies_list')
        else:
            messages.error(request, "Incorrect username or password. Please try again.")

    return render(request, 'login.html')


def logoutV(request):
    logout(request)
    return redirect('login')
