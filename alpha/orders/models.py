from django.db import models
from products.models import *
from django.contrib.auth.models import User


class OrderDeliveryArea(models.Model):
    name = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
    area_ref = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
    is_active = models.BooleanField(
        default=True)
    updated = models.DateTimeField(
        auto_now_add=False, 
        auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Регион доставки"
        verbose_name_plural = "Регионы доставки"


class OrderDeliveryCity(models.Model):
    area = models.ForeignKey(
        OrderDeliveryArea,
        blank=True, 
        null=True, 
        default=None, 
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
    city_ref = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
    is_active = models.BooleanField(
        default=True)
    updated = models.DateTimeField(
        auto_now_add=False, 
        auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Город доставки"
        verbose_name_plural = "Города доставки"


class Status(models.Model):
    name = models.CharField(
        max_length=24, 
        blank=True, 
        null=True, 
        default=None)
    is_active = models.BooleanField(
        default=True)
    created = models.DateTimeField(
        auto_now_add=True, 
        auto_now=False)
    updated = models.DateTimeField(
        auto_now_add=False, 
        auto_now=True)

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = "Статус заказа"
        verbose_name_plural = "Статусы заказа"


class Order(models.Model):
    session_key = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
    user = models.ForeignKey(
        User, 
        blank=True, 
        null=True, 
        default=None, 
        on_delete=models.CASCADE)
    total_order_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0)
    customer_name = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        default=None)
    customer_email = models.EmailField(
        blank=True, 
        null=True, 
        default=None)
    customer_phone = models.CharField(
        max_length=48, 
        blank=True, 
        null=True, 
        default=None)
    customer_address = models.TextField(
        blank=True, 
        null=True, 
        default=None)
    comments = models.TextField(
        blank=True, 
        null=True, 
        default=None)
    status = models.ForeignKey(
        Status, 
        on_delete=models.CASCADE)
    created = models.DateTimeField(
        auto_now_add=True, 
        auto_now=False)
    updated = models.DateTimeField(
        auto_now_add=False, 
        auto_now=True)
    is_active = models.BooleanField(
        default=True)

    def __str__(self):
        return "Заказ %s" % self.id

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE)
    quantity = models.IntegerField(
        default=0)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0)
    order_item_subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0)
    is_active = models.BooleanField(
        default=True)
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False)
    updated = models.DateTimeField(
        auto_now_add=False,
        auto_now=True)

    def __str__(self):
        return "Товар в заказе %s" % self.product.name

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"
        