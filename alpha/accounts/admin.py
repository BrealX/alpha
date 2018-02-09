from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
	class Meta:
		model = Customer

	list_display = [field.name for field in Customer._meta.fields]
	search_fields = ('user',)
	ordering = ('user',)


admin.site.register(Customer, CustomerAdmin)