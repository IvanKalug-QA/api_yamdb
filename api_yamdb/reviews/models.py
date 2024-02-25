from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

ROOT = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role='user',
                    bio=None):
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, role=role
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, role='admin',
                         bio=None):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            role=role,
            is_superuser=1
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
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
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(default='user',
                            blank=True, max_length=25, choices=ROOT)
    is_superuser = models.IntegerField(max_length=1, default=0, blank=True)
    password = None
    last_login = None

    objects = UserManager()

    REQUIRED_FIELDS = ['email']

    USERNAME_FIELD = 'username'
