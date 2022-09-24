from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (

        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
       
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, default='customer', max_length=50)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']