from django.db import models


class Category(models.Model):
    nomi=models.CharField(max_length=100)

    def __str__(self):
        return self.nomi


class Product(models.Model):
    nomi=models.CharField(max_length=100)
    izoh=models.TextField()
    narxi=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    ombor=models.IntegerField(default=0)

    def __str__(self):
        return self.nomi

    def is_in_ombor(self):
        return self.ombor > 0

    def olish_ombor(self, zakas):
        if zakas > self.ombor:
            return False

        self.ombor -= zakas
        self.save()
        return True

    def qoshish_ombor(self, soni):
        self.ombor += soni
        self.save()

    class Meta:
        ordering=['nomi']
