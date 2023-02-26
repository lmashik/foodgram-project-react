from django.core.exceptions import ValidationError


def validate_me(value):
    """Проверка равенства значения строке 'me'."""
    if value == 'me':
        raise ValidationError(
            'Using me as a username is not allowed.'
        )
    return value
