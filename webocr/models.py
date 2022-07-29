from django.contrib.auth.models import User
import django.utils.timezone
from django.core.exceptions import ValidationError
from django.db import models
# from django.utils import timezone


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=200, default='Not Available')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}, {self.category.name}, {self.price}"

    def refill(self):
        self.stock += 100

    def save(self, *args, **kwargs):
        if self.stock < 0 or self.stock > 1000:
            ValidationError('Value of stock must be in between 0 and 1000')
        super().save(*args, **kwargs)

    def clean(self):
        super(Product, self).clean()
        if self.stock < 0 or self.stock > 1000:
            ValidationError('Value of stock must be in between 0 and 1000')


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]
    company = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return f"{'name=' + self.username, 'shipping_address=' + self.shipping_address}"


class Order(models.Model):
    ORDER_VALUES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered')
    ]
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='clients', on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=ORDER_VALUES, default=1)
    status_date = models.DateField(default=django.utils.timezone.now, blank=True)
    tot_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{'product=' + str(self.product.name) + ', client=' + str(self.client.username) + ', num_units' + str(self.num_units) +', order_status=' + str(self.ORDER_VALUES[self.order_status][1]) + ', status_date=' + str(self.status_date)}"

    def total_cost(self):
        return f"{self.num_units * self.product.price}"

    def save(self, *args, **kwargs):
        self.tot_cost = self.total_cost()
        super().save(*args, **kwargs)
