from django.conf import settings
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from django.views.generic.base import View

from account.form import CustomUserCreationForm, AddressForm, PhoneNumberForm, SignIn, SignInViaUsernameForm


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

class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)

class LogInView(GuestOnlyView, FormView):
    template_name = 'account/logIn.html'
    form_class = SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if not form.cleaned_data['remember_me']:
            request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect('home')