from re import L
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from xlib.abstract.models import AbstractModel


class UserManager(BaseUserManager):
    """User model manager"""

    def create_user(self, username, email, position, first_name, last_name, password=None):
        """Create and return a User with an Username, an email and a password"""
        if username is None:
            return ValueError("User must have an username")
        if email is None:
            return ValueError("User must have an email")
        
        email=self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, position=position)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, position, first_name, last_name, password):
        """Create and return a User with admin permissions"""
        user = self.create_user(username=username, email=email, first_name=first_name, last_name=last_name, position=position, password=password,)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, AbstractModel, PermissionsMixin):
    """User database model class"""
    
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    position = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username' # User will login with username and password
    REQUIRED_FIELDS = ['email', 'position']

    def __str__(self):
        return f'{self.public_id}_{self.username}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
