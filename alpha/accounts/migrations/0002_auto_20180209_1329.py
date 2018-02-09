# Generated by Django 2.0.1 on 2018-02-09 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={},
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
        migrations.AddField(
            model_name='customer',
            name='banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='delivery_address',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='register_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата регистрации'),
        ),
    ]
