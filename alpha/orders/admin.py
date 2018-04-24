from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    fields = ["product", "quantity", "price", "order_item_subtotal", "is_active"]


class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order

    inlines = [OrderItemInline]
    list_display = [field.name for field in Order._meta.fields]
    exclude = ('session_key',)


admin.site.register(Order, OrderAdmin)


class StatusAdmin(admin.ModelAdmin):
    class Meta:
        model = Status

    list_display = [field.name for field in Status._meta.fields]


admin.site.register(Status, StatusAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    class Meta:
        model = OrderItem

    list_display = [field.name for field in OrderItem._meta.fields]


admin.site.register(OrderItem, OrderItemAdmin)


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
