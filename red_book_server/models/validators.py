from django.core.exceptions import ValidationError


def check_positive_number(number: int | float):
    if number < 0:
        raise ValidationError(
            'The passed number must be greater than or equal to 0!',
            params={'number': number}
        )