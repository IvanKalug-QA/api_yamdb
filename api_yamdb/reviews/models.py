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
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, role=role
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, role=None,
                         bio=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            bio=bio,
        )
        user.role = 'admin'
        user.is_superuser = 1
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
