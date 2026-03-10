from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.

def index(request):

    return redirect('login')

def signUp(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request," The account created successfully !!")
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request,'signUp.html',{'form':form})

def loginV(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        u= authenticate(request,username=username,password=password)

        if u is not None:
            login(request,u)
            return redirect('movies')

        else:
            messages.error(request,"Incorect username or password try agin ")

    return render(request,'login.html')


def logoutV(request):
    logout(request)
    return redirect('login')