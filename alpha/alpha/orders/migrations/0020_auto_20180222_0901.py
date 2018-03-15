# Generated by Django 2.0.1 on 2018-02-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_auto_20180221_1015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='total_order_amount',
        ),
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
