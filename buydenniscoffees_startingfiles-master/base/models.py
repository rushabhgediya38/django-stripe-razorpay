from django.db import models

# Create your models here.


class Coffee_razorpay(models.Model):
    name = models.CharField(max_length=254)
    amount = models.CharField(max_length=254)
    payment_id = models.CharField(max_length=14)
    razorpay_id = models.CharField(max_length=100, blank=False, null=True)
    payment_done = models.BooleanField(default=False)

    def __str__(self):
        return self.name