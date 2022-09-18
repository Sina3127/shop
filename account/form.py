from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from account.models import Address


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = get_user_model()
		fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = get_user_model()
		fields = ('email', 'username',)

class AddressForm(ModelForm):
	class Meta:
		model = Address
		fields = ('address', )