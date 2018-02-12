from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	class Meta:
		model = Profile

	list_display = [field.name for field in Profile._meta.fields]
	search_fields = ('user',)
	ordering = ('user',)


admin.site.register(Profile, ProfileAdmin)