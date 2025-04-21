from django.db import models

# Create your models here.

class LibraryItem(models.Model):
    title = models.CharField(max_length=200)
    category = models.TextField(default='')
    photo = models.ImageField(default='img/default.png')
    period = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    description = models.TextField(default='No description available')
    owner = models.CharField(max_length=100, default='')
    owner_rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    product_rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    created_at = models.DateTimeField(auto_now_add=True)
    rented_by = models.CharField(max_length=100, default='')

regular_user = {"username": "rick", "password": "regular"}
admin_user = {"username": "andy", "password": "admin"}