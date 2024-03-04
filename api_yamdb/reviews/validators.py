from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Валидация года выпуска произведения."""
    this_year = timezone.now().year
    if value > this_year:
        raise ValidationError(
            'Год выпуска произведения не может '
            f'быть больше {this_year}'
        )
