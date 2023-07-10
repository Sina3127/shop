from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from account.models import Address, PhoneNumber, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'avatar')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'avatar')

class UserCacheMixin:
    user_cache = None

class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('You entered an invalid password.'))

        return password

class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('Username'))

    @property
    def field_order(self):
        return ['username', 'password', 'remember_me']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = CustomUser.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('You entered an invalid username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return username

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('address',)

    def __init__(self, user, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        self.instance.user = self.user
        super(AddressForm, self).save(commit)


class PhoneNumberForm(ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number',)

    def __init__(self, user, *args, **kwargs):
        super(PhoneNumberForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        self.instance.user = self.user
        super(PhoneNumberForm, self).save(commit)

