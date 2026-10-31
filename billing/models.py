from django.db import models
from products.models import Order

class Payment(models.Model):
    order=models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    tolov_id=models.CharField(max_length=50)
    qancha=models.DecimalField(max_digits=10, decimal_places=10)
    qachon=models.DateTimeField(auto_now_add=True)
    
