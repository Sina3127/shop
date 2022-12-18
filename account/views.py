from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import generic
from .models import Address

from account.form import CustomUserCreationForm, AddressForm


def changePassword(request):  # password, you may also like, new password, confirm no password
    pass


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, "account/signup.html", {'form': form})


def addLocation(request):  # locations, you may also like
    if request.method == 'POST':
        form = AddressForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AddressForm(request.user)
    return render(request, "account/addLocation.html", {'form': form})


def removeLocation(request):  # locations, you may also like
    pass


def profile(request):
    if request.user.is_authenticated:
        page = loader.get_template('account/profile.html')
        context = {
        }
        return HttpResponse(page.render(context, request))
    else:
        return redirect('signup')
