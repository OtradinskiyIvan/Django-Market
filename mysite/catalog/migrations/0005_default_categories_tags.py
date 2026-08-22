from django.db import migrations

DEFAULT_CATEGORIES = ['tech', 'home', 'style']
DEFAULT_TAGS = ['exclusive', 'eco', 'gift', 'smart', 'compact']


def create_defaults(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Tag = apps.get_model('catalog', 'Tag')
    for slug in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(slug=slug, defaults={'title': slug})
    for slug in DEFAULT_TAGS:
        Tag.objects.get_or_create(slug=slug, defaults={'title': slug})


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_order_status'),
    ]

    operations = [
        migrations.RunPython(create_defaults, migrations.RunPython.noop),
    ]
