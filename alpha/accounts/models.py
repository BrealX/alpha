from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE,
		related_name='profile'
	)
	phone = models.CharField(
		null=True,
		blank=True,
		max_length=40
		)
	register_date = models.DateField(
		auto_now_add=True,
		null=True
	)
	delivery_address = models.CharField(
		max_length=150,
		null=True,
		blank=True
	)


	def __str__(self):
		return "Клиент %s" % self.user.username


	def user_email(self):
		return self.user.email


	def user_username(self):
		return self.user.username


	class Meta:
		verbose_name = "Клиент"
		verbose_name_plural = "Клиенты"