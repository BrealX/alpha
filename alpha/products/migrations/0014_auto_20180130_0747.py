# Generated by Django 2.0.1 on 2018-01-30 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_product_is_on_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='is_on_stock',
            new_name='is_in_stock',
        ),
    ]