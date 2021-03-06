from django.contrib import admin
from .models import *


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order

    list_display = [field.name for field in Order._meta.fields]
    inlines = [ProductInOrderInline]


admin.site.register(Order, OrderAdmin)


class StatusAdmin(admin.ModelAdmin):
    class Meta:
        model = Status

    list_display = [field.name for field in Status._meta.fields]


admin.site.register(Status, StatusAdmin)


class ProductInOrderAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductInOrder

    list_display = [field.name for field in ProductInOrder._meta.fields]


admin.site.register(ProductInOrder, ProductInOrderAdmin)


class ProductInBasketAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductInBasket

    list_display = [field.name for field in ProductInBasket._meta.fields]


admin.site.register(ProductInBasket, ProductInBasketAdmin)


class OrderDeliveryAreaAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderDeliveryArea

    list_display = [field.name for field in OrderDeliveryArea._meta.fields]
    list_filter = ['name', ]
    search_fields = ['name', 'id']


admin.site.register(OrderDeliveryArea, OrderDeliveryAreaAdmin)


class OrderDeliveryCityAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderDeliveryCity

    list_display = [field.name for field in OrderDeliveryCity._meta.fields]
    list_filter = ['area', 'name', ]
    search_fields = ['area', 'name', 'id', 'city_ref', ]


admin.site.register(OrderDeliveryCity, OrderDeliveryCityAdmin)