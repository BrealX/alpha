from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE
	)
	email = models.EmailField(
		'Электронная почта',
		max_length=255,
		unique=True,
	)
	name = models.CharField(
		'Имя',
		max_length=40,
		null=True,
		blank=True
	)
	register_date = models.DateField(
		'Дата регистрации',
		auto_now_add=True
	)
	is_active = models.BooleanField(
		'Активен',
		default=True
	)
	delivery_address = models.CharField(
		'Адрес доставки',
        max_length=400,
        null=True,
        blank=True
    )

	def __str__(self):
		return "%s %s" % (self.email, self.name)

	objects = User()

	class Meta:
		verbose_name = "Пользователь"
		verbose_name_plural = "Пользователи"
