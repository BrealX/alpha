# Generated by Django 2.0.1 on 2018-01-19 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20180119_1301'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_amount',
            new_name='total_price',
        ),
        migrations.RenameField(
            model_name='productinorder',
            old_name='total_amount',
            new_name='total_price',
        ),
    ]