# Generated by Django 2.0.1 on 2018-01-19 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productinorder',
            options={'verbose_name': 'Заказанный товар', 'verbose_name_plural': 'Заказанные товары'},
        ),
    ]