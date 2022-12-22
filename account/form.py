from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from account.models import Address, PhoneNumber


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
		fields = ('address', )

class PhoneNumberForm(ModelForm):
	class Meta:
		model = PhoneNumber
		fields = ('phone_number', )