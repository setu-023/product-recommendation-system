from turtle import update
from django.db import models

class Weather(models.Model):
   
    WEATHER_TYPE_CHOICES = (

        ('normal', 'Normal'),
        ('hot', 'Hot'),
        ('cold', 'Cold'),
       
    )
    name = models.CharField(max_length=55, unique=True)
    weather_type = models.CharField(choices=WEATHER_TYPE_CHOICES, default='customer', max_length=50)
    high_range = models.IntegerField()
    low_range = models.IntegerField()
    STATUS_TYPE_CHOICES = (

        ('active', 'Active'),
        ('inactive', 'Inactive'),       
    )
    status = models.CharField(choices=STATUS_TYPE_CHOICES, default='active', max_length=55)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)