from django.forms import ModelForm

from shop.models import ReviewComment


class AddReview(ModelForm):
    class Meta:
        model = ReviewComment
        fields = ('text', 'point', )