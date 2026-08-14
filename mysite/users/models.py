from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    class Role(models.IntegerChoices):
         CUSTOMER = 0, 'Customer'
         SELLER = 1, 'Seller'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=255)
    role = models.IntegerField(choices=Role.choices, default=Role.CUSTOMER)
    is_verified = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    favorites = models.ManyToManyField('catalog.Catalog', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
          return f"{self.get_role_display()} {self.name}"


class SellerReview(models.Model):
     customer = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, related_name='review_given', null=True)
     seller = models.ForeignKey('users.Profile', on_delete=models.SET_NULL, related_name='review_received', null=True)
     rating = models.PositiveSmallIntegerField(
          validators=[MinValueValidator(1), MaxValueValidator(5)],
     )
     created_at = models.DateTimeField(auto_now_add=True)
     comment = models.TextField(blank=True)
     updated_at = models.DateTimeField(auto_now=True)
