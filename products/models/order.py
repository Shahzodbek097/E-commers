from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .product import Product

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqam formatda bolsin: '+998xxxxxxxxx'."
)

class Order(models.Model):
    PENDING = 'Pending'         #zakas ko'rib chiqilmoqda
    PROCESSING = 'Processing'   #jarayonda
    SHIPPED = 'Shipped'         #yuklandi
    DELIVERED = 'Delivered'     #yetkazildi
    CANCELED = 'Canceled'       #bekor qilindi

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    buyurtmachi=models.ForeignKey(User, on_delete=models.CASCADE)
    nechta=models.IntegerField()
    qachon=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=35, choices=STATUS_CHOICES, default=PENDING)
    phone_number=models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    is_paid=models.BooleanField(default=False)

    def set_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError('Invalid status')
        self.status=new_status
        self.save()

    def is_transition_allowed(self, new_status):
        allowed_transitions = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED],
        }

        return new_status in allowed_transitions.get(self.status, [])

    def __str__(self):
        return f"Order({self.product.nomi} by {self.buyurtmachi.username})"




