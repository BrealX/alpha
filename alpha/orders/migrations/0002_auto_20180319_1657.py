# Generated by Django 2.0.3 on 2018-03-19 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('order_item_subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'verbose_name_plural': 'Товары в заказе',
                'verbose_name': 'Товар в заказе',
            },
        ),
        migrations.RemoveField(
            model_name='productinbasket',
            name='order',
        ),
        migrations.RemoveField(
            model_name='productinbasket',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productinorder',
            name='order',
        ),
        migrations.RemoveField(
            model_name='productinorder',
            name='product',
        ),
        migrations.DeleteModel(
            name='ProductInBasket',
        ),
        migrations.DeleteModel(
            name='ProductInOrder',
        ),
    ]