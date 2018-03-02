from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        max_length=64, 
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

    def price_with_discount(self):
        return float(self.price) - (float(self.price) * float(self.discount) / 100)  


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        blank=True, 
        null=True, 
        default=None, 
        on_delete=models.CASCADE, 
        related_name='images')
    image = models.ImageField(
        upload_to='static/products_images/')
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