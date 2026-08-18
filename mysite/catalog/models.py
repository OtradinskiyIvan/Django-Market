from django.db import models

class AvailabilityManeger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=Catalog.Status.AVAILABLE)

class Catalog(models.Model):
    class Status(models.IntegerChoices):
        ARCHIVED = 0,
        AVAILABLE = 1,

    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    seller = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True) 
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=10)
    slug = models.SlugField(max_length=255, unique=True)
    desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(choices=Status.choices, default=Status.AVAILABLE)

    objects = models.Manager()
    available = AvailabilityManeger()

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey('users.Profile', on_delete=models.CASCADE,  related_name='orders')
    is_shipped = models.BooleanField(default=False)
    shipped_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order id:" + str(self.pk)

    @property
    def total(self):
        return sum(oi.line_total for oi in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Catalog', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()

    def __str__(self):
        return f"Order: {str(self.order)}; Item: {str(self.item)}"

    @property
    def line_total(self):
        return self.price * self.quantity


class ItemImage(models.Model):
    item = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/images/')


class ItemVideo(models.Model):
    item = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name='video')
    video = models.FileField(upload_to='items/video/')
