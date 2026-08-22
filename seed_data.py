from pathlib import Path
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile, SellerReview
from catalog.models import Catalog, Category, Tag, ItemImage, ItemVideo, Order, OrderItem

IMG_DIR = Path('/home/ivan/Projects/Django_course/testproj/mysite/catalog/static/catalog/img')


def get_profile(username, first_name, last_name, email, phone, role, password, balance=0):
    user, _ = User.objects.get_or_create(username=username)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.set_password(password)
    user.is_active = True
    user.save()
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.phone = phone
    profile.role = role
    profile.balance = balance
    profile.is_verified = True
    profile.save()
    return profile


seller = get_profile('ivan', 'Иван', 'Петров', 'ivan@example.com', '+70000000000',
                     Profile.Role.SELLER, 'secret123')
buyer = get_profile('petr', 'Петя', 'Иванов', 'petr@example.com', '+70000000001',
                    Profile.Role.CUSTOMER, 'secret123', balance=1000)

smart, _ = Category.objects.get_or_create(title='Смартфоны', slug='smartphones')
laptops, _ = Category.objects.get_or_create(title='Ноутбуки', slug='notebooks')
desktops, _ = Category.objects.get_or_create(title='Компьютеры', slug='desktops')
new_tag, _ = Tag.objects.get_or_create(title='New', slug='new')


def make_item(category, title, slug, price, filename, qty=10, desc=''):
    item, created = Catalog.objects.get_or_create(
        slug=slug,
        defaults=dict(category=category, seller=seller, title=title,
                      price=price, quantity=qty, desc=desc),
    )
    if created and filename:
        img = ItemImage(item=item)
        with open(IMG_DIR / filename, 'rb') as f:
            img.image.save(filename, File(f))
    return item


# 1. Через форму (залогиненный клиент) — проверяет всю цепочку add_item + файлы
mac = make_item(laptops, 'MacBook Air', 'macbook-air', 1299, 'laptop.jpeg')
pc = make_item(desktops, 'Gaming PC', 'gaming-pc', 799, 'pc.jpeg')

c = Client()
assert c.login(username='ivan', password='secret123'), 'login failed'

with open(IMG_DIR / 'iphone.jpeg', 'rb') as f:
    iphone_file = SimpleUploadedFile('iphone.jpeg', f.read(), content_type='image/jpeg')
dummy_video = SimpleUploadedFile('demo.mp4', b'placeholder-mp4', content_type='video/mp4')

r = c.post('/catalog/add_item/', {
    'title': 'iPhone 16', 'slug': 'iphone-16',
    'price': 999, 'quantity': 5, 'desc': 'Test upload through the form',
    'is_available': 'on',
    'category': smart.id, 'tags': new_tag.id,
    'images': [iphone_file], 'video': dummy_video,
}, HTTP_HOST='127.0.0.1')
print('POST add_item status:', r.status_code)
iphone = Catalog.objects.filter(slug='iphone-16').first()

# 2. Избранное покупателя
buyer.favorites.add(iphone, mac)

# 3. Отзыв покупателя на продавца
SellerReview.objects.get_or_create(
    customer=buyer, seller=seller,
    defaults=dict(rating=5, comment='Отличный продавец!'),
)

# 4. Тестовые заказы со статусами (для Этапа 6)
def make_order(buyer, status, items, balance=False):
    if balance:
        seller.balance += sum(price * qty for _, price, qty in items)
        seller.save()
    order = Order.objects.create(user=buyer, status=status)
    for item, price, qty in items:
        OrderItem.objects.create(order=order, item=item, quantity=qty, price=price)
    return order

if not Order.objects.exists():
    ordered = make_order(buyer, Order.Status.ORDERED, [(pc, 799, 1)])
    shipped = make_order(buyer, Order.Status.SHIPPED, [(mac, 1299, 1)])
    shipped.shipped_at = timezone.now()
    shipped.save(update_fields=['shipped_at'])
    accepted = make_order(buyer, Order.Status.ACCEPTED, [(iphone, 999, 1)], balance=True)
    accepted.closed_at = timezone.now()
    accepted.save(update_fields=['closed_at'])

print('User:', User.objects.count(), '| Profile:', Profile.objects.count())
print('Catalog:', Catalog.objects.count(), '| ItemImage:', ItemImage.objects.count(),
      '| ItemVideo:', ItemVideo.objects.count(), '| SellerReview:', SellerReview.objects.count())
print('buyer favorites:', list(buyer.favorites.values_list('title', flat=True)))
print('Orders:', [(o.status, list(o.orderitem_set.values_list('item__title', 'quantity'))) for o in buyer.orders.all()])

import boto3
from django.conf import settings
s3 = boto3.client('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                  region_name=settings.AWS_S3_REGION_NAME)
print('keys:', [o['Key'] for o in s3.list_objects_v2(Bucket='media').get('Contents', [])])