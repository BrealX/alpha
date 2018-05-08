# Generated by Django 2.0.3 on 2018-04-23 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_remove_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='delivery_area',
            field=models.OneToOneField(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.OrderDeliveryArea'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='delivery_city',
            field=models.OneToOneField(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.OrderDeliveryCity'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]