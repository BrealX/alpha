# Generated by Django 2.0.2 on 2018-03-02 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_is_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=240, null=True),
        ),
    ]