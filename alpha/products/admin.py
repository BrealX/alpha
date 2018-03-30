from django.contrib import admin
from .models import *
from django.forms import TextInput, Textarea


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    fields = ["user", "text", "score", "is_featured", "is_active"]


class ProductCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductCategory

    list_display = [field.name for field in ProductCategory._meta.fields]
    list_filter = ['name', ]
    search_fields = ['name', 'id']

admin.site.register(ProductCategory, ProductCategoryAdmin)



class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product

    inlines = [ReviewInline]
    list_display = [field.name for field in Product._meta.fields]
    list_filter = ['name', ]
    search_fields = ['name', 'id']

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductImage

    list_display = [field.name for field in ProductImage._meta.fields]


admin.site.register(ProductImage, ProductImageAdmin)


class ReviewAdmin(admin.ModelAdmin):
    class Meta:
        model = Review

admin.site.register(Review, ReviewAdmin)
