import re
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The username field must be set!")

        # Validate if the username is a valid email or phone number
        if re.match(r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$',
                    username):  # Email validation
            username = self.normalize_email(username)
        else:  # Phone number validation
            phone_regex = r'^\+?880\d{10}$'  # Bangladeshi phone number regex
            phone_validator = RegexValidator(
                regex=phone_regex,
                message="Enter a valid Bangladeshi phone number."
            )
            phone_validator(username)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
