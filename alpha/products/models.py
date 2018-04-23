from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class ProductCategory(models.Model):
    name = models.CharField(
        max_length=128, 
        blank=True, 
        null=True, 
        default=None)
    description = models.CharField(
        max_length=240,
        blank=True,
        null=True,
        default=None)
    is_active = models.BooleanField(
        default=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категория товаров"

    def get_related_products(self):
        return self.product_set.filter(is_active=True)


class Product(models.Model):
    name = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        default=None)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0)
    discount = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=0)
    category = models.ForeignKey(
        ProductCategory, 
        blank=True, 
        null=True, 
        default=None, 
        on_delete=models.CASCADE)
    short_description = models.TextField(
        blank=True, 
        null=True, 
        default=None)
    description = models.TextField(
        blank=True, 
        null=True, 
        default=None)
    description_age = models.TextField(
        blank=True, 
        null=True, 
        default=None)
    description_content = models.TextField(
        blank=True, 
        null=True, 
        default=None)
    description_package_size = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        default=None)
    description_product_size = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        default=None)
    description_package_type = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        default=None)
    description_battery = models.CharField(
        max_length=64, 
        blank=True, 
        null=True, 
        default=None)
    is_active = models.BooleanField(
        default=True)
    is_new = models.BooleanField(
        default=False)
    is_in_stock = models.BooleanField(
        default=True)
    is_on_demand = models.BooleanField(
        default=False)
    created = models.DateTimeField(
        auto_now_add=True, 
        auto_now=False)
    updated = models.DateTimeField(
        auto_now_add=False, 
        auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    
    @property
    def product_main_image(self):
        return self.images.get(is_main=True)

    @property
    def product_all_images(self):
        return (self.images.get(is_main=False),) 

    @property
    def price_with_discount(self):
        price_with_discount = self.price - (self.price * self.discount / 100)  
        return "%.2f" % price_with_discount


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        blank=True, 
        null=True, 
        default=None, 
        on_delete=models.CASCADE, 
        related_name='images')
    image = models.ImageField(
        upload_to='static/products/img/')
    is_main = models.BooleanField(
        default=False)
    is_active = models.BooleanField(
        default=True)
    created = models.DateTimeField(
        auto_now_add=True, 
        auto_now=False)
    updated = models.DateTimeField(
        auto_now_add=False, 
        auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class Review(models.Model):
    user = models.ForeignKey(
        User, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL)
    product = models.ForeignKey(
        Product, 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL)
    order = models.ForeignKey(
        'orders.Order', 
        blank=True, 
        null=True, 
        on_delete=models.SET_NULL)
    text = models.TextField()
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s: оценен на %s пользователем %s" % (self.product.name, self.score, self.user.username)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created']

    def get_user(self):
        return self.user
