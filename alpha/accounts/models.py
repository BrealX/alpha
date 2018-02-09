from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
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
		'Дата регистрации',
		auto_now_add=True,
		null=True
	)
	delivery_address = models.CharField(
		'Адрес доставки',
		max_length=150,
		null=True,
		blank=True
	)
	banned = models.BooleanField(
		default=False
	)

	def __str__(self):
		return "Клиент %s" % self.user.username

	class Meta:
		verbose_name = "Клиент"
		verbose_name_plural = "Клиенты"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.customer.save()
