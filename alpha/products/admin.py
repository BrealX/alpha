from django.contrib import admin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

    list_display = [field.name for field in Product._meta.fields]
    list_filter = ['name', ]
    search_fields = ['name', 'id']
    inlines = [ProductImageInline]


admin.site.register(Product, ProductAdmin)


class ProductInOrderAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductImage

    list_display = [field.name for field in ProductImage._meta.fields]


admin.site.register(ProductImage, ProductInOrderAdmin)