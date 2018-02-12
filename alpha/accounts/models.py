from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE
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

	class Meta:
		verbose_name = "Клиент"
		verbose_name_plural = "Клиенты"