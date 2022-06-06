import email
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# from .manager import *

# class CustomUser(AbstractUser):
#     username = None
#     email=models.EmailField(unique=True)
#     Phone_number = models.CharField(max_length=12,null=True)
#     is_email_verified = models.BooleanField(default=False)
#     otp  = models.CharField(max_length=4,null=True,blank=True)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


class MyAccountManager(BaseUserManager):
    def create_user(self,  email, first_name,last_name, phone_number,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        

        user = self.model(
            email=self.normalize_email(email),
            
            first_name=first_name,
            last_name=last_name,
            phone_number = phone_number,
            





        )

        user.set_password(password)
        

        user.save(using=self._db)
        return user

    def create_superuser(self,  email,first_name,last_name, username, phone_number,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number = phone_number,
            password=password,

            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    username = models.CharField(unique=False, max_length=50)
    email = models.EmailField(unique=True, max_length=50)
    phone_number = models.CharField(max_length=13)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True)
    uid = models.UUIDField(default=uuid.uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
