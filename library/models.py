from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.

class LibraryItem(models.Model):
    title = models.CharField(max_length=200)
    category = models.TextField(default='')
    photo = models.ImageField(default='img/default.png')
    period = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    description = models.TextField(default='No description available')
    owner = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    product_rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    created_at = models.DateTimeField(auto_now_add=True)
    rented_by = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('library:item-detail', args=[self.id])
