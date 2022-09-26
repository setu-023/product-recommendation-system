import imp
from django.db import models
from account.models import CustomUser

class Product(models.Model):

    name   = models.CharField(max_length=255, )
    owner  = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    quatity  = models.IntegerField()
    price  = models.IntegerField()
    weather_tag = models.JSONField(null=True, blank=True)
    STATUS_TYPE_CHOICES = (

        ('active', 'Active'),
        ('inactive', 'Inactive'),       
    )
    status = models.CharField(choices=STATUS_TYPE_CHOICES, default='active', max_length=55)

    created_at = models.DateField(auto_now_add = True)
    updated_at  = models.DateField(auto_now = True)

    def __str__(self):
        return self.name