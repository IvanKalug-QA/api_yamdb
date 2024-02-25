from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

ROOT = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Enter a valid username.',
                code='invalid_username'
            )
        ]
    )
    bio = models.TextField(blank=True)
    role = models.CharField(default='user',
                            blank=True, max_length=25, choices=ROOT)
    password = None
    last_login = None

    REQUIRED_FIELDS = ['email']

    USERNAME_FIELD = 'username'
