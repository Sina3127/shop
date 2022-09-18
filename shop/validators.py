from django.core.exceptions import ValidationError


def point_validator(value):
    if value < 1:
        raise ValidationError('value must be greater or equal to 1')
    if value > 5:
        raise ValidationError('value must be less than or equal to 5')