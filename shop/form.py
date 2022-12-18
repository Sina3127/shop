import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, DateField, ModelChoiceField, SelectDateWidget

from account.models import Address
from shop.models import ReviewComment


class AddReview(ModelForm):
    class Meta:
        model = ReviewComment
        fields = ('text', 'point',)


def present_or_future_date(value):
    if value < datetime.date.today():
        raise ValidationError("The date cannot be in the past!")
    return value


class AddTransaction(Form):
    send_time = DateField(widget=SelectDateWidget(), validators=(present_or_future_date,))
    address = ModelChoiceField(queryset=Address.objects.all())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].queryset = self.fields['address'].queryset.filter(user=user)
