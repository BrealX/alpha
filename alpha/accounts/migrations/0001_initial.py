# Generated by Django 2.0.3 on 2018-03-14 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=40, null=True)),
                ('register_date', models.DateField(auto_now_add=True, null=True)),
                ('delivery_address', models.CharField(blank=True, max_length=150, null=True)),
                ('receiver_name', models.CharField(blank=True, max_length=240, null=True)),
                ('activation_key', models.CharField(blank=True, max_length=240, null=True)),
                ('key_expires', models.DateTimeField(blank=True, null=True)),
                ('delivery_area', models.OneToOneField(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.OrderDeliveryArea')),
                ('delivery_city', models.OneToOneField(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.OrderDeliveryCity')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Клиенты',
                'verbose_name': 'Клиент',
            },
        ),
    ]
