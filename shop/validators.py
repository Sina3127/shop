from django.core.exceptions import ValidationError


def point_validator(value):
    if value < 1:
        raise ValidationError('value must be greater or equal to 1')
    if value > 5:
        raise ValidationError('value must be less than or equal to 5')

def validate_minimum_size(width=None, height=None):
    def validator(image):
        error = False
        if width is not None and image.width < width:
            error = True
        if height is not None and image.height < height:
            error = True
        if error:
            raise ValidationError(
                [f'Size should be at least {width} x {height} pixels.']
            )

    return validator