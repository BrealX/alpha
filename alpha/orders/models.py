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
        return "Заказ %s %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)    


class ProductInOrder(models.Model):
    session_key = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
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
    qnty = models.IntegerField(
        default=1)
    price_per_item = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0)
    total_amount = models.DecimalField(
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

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_amount = int(self.qnty) * price_per_item
        super(ProductInOrder, self).save(*args, **kwargs)        
        order = self.order
        all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)
        order_total_amount = 0
        for item in all_products_in_order:
            order_total_amount += item.total_amount
        self.order.total_order_amount = order_total_amount
        self.order.save(force_update=True)


class ProductInBasket(models.Model):
    session_key = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
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
    qnty = models.IntegerField(
        default=1)
    price_per_item = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0)
    total_price = models.DecimalField(
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
        return "%s" % self.product.name

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def save(self, *args, **kwargs):
        self.price_per_item = self.product.price - (self.product.price * self.product.discount / 100)
        self.total_price = float(self.qnty) * float(self.price_per_item)
        super(ProductInBasket, self).save(*args, **kwargs) 