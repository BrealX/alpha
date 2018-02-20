from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
	class Meta:
		model = Profile

	list_display = ('user_username', 'user_email', 'phone', 'delivery_address')
	#or [field.name for field in Profile._meta.fields] for all fields to show
	search_fields = ('user',)
	ordering = ('user',)


admin.site.register(Profile, ProfileAdmin)