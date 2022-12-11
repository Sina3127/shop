from django.forms import ModelForm, Form, DateField, ModelChoiceField
from account.models import Address
from shop.models import ReviewComment


class AddReview(ModelForm):
    class Meta:
        model = ReviewComment
        fields = ('text', 'point',)


class AddTransaction(Form):
    send_time = DateField()
    address = ModelChoiceField(queryset=Address.objects.all())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address.queryset = self.address.queryset.filter(user=user)
