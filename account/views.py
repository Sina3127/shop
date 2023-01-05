from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic

from account.form import CustomUserCreationForm, AddressForm, PhoneNumberForm, LogInForm


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


def removeLocation(request, id):  # locations, you may also like
    pass


def removePhoneNumber(request, id):  # locations, you may also like
    pass


def profile(request):
    if request.user.is_authenticated:
        page = loader.get_template('account/profile.html')
        context = {
        }
        return HttpResponse(page.render(context, request))
    else:
        return redirect('signup')


def addPhoneNumber(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PhoneNumberForm(request.user)
    return render(request, "account/addPhoneNumber.html", {'form': form})


class LogOut(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class LogIn(generic.FormView):
    form_class = LogInForm
    template_name = 'account/logIn.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(LogIn, self).form_valid(form)