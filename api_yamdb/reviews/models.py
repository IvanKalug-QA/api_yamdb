from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user =self.model(
            username=username, email=email
        )
        user.set_unusable_password()
        user.save()
        return user
    
    def create_superuser(self, email, username):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username
        )
        user.role = 'admin'
        user.save(using=self._db)
        return user
        

class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(default='user', blank=True, max_length=25)
    password = None

    objects = UserManager()

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
