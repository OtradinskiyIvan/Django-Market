from django.db import models


class AvailabilityManeger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=Catalog.Status.AVAILABLE)

class Catalog(models.Model):
    class Status(models.IntegerChoices):
        ARCHIVED = 0,
        AVAILABLE = 1,

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    slug = models.SlugField(max_length=255, unique=True)
    desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(choices=Status.choices, default=Status.AVAILABLE)

    objects = models.Manager()
    available = AvailabilityManeger()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE,  related_name='orders')
    is_shipped = models.BooleanField(default=False)
    shipped_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Catalog', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

