import uuid
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin,BaseUserManager)
from phonenumber_field.modelfields import PhoneNumberField



class UserManager(BaseUserManager):
    #Method to create a regular user
    def create_user(self, email, phone_number, username, password=None, **extra_fields):
        # Check if user email is provided
        if not email:
            raise ValueError("Users must have an email")
        # Normalize user email
        email = self.normalize_email(email)
        # Create and save the user
        user = self.model(email=email, username=username,phone_number=phone_number,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Method to create a superuser
    def create_superuser(self, username, email,phone_number, password=None, **extra_fields):
        user = self.create_user(username, email,phone_number, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('blogger', 'Blogger'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=ROLES, default='blogger')
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "phone_number","last_name","role"]

    def __str__(self):
        return self.email
    
    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

