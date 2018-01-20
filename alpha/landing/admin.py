from django.contrib import admin
from .models import *


class SubscriberAdmin(admin.ModelAdmin):
    class Meta:
        model = Subscriber

    list_display = [field.name for field in Subscriber._meta.fields]
    list_filter = ['name']
    search_fields = ['name', 'email']


admin.site.register(Subscriber, SubscriberAdmin)

