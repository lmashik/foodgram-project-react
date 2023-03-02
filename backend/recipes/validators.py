from django.core.exceptions import ValidationError


def validate_time(value):
    """Проверка времени приготовления."""
    if value < 1:
        raise ValidationError(
            'Invalid cooking time'
        )
    return value
