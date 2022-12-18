from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from account.models import Address


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'avatar')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'avatar')


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
