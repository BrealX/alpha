from django.db import models
from django.contrib.auth.models import User
from orders.models import OrderDeliveryArea, OrderDeliveryCity


class Profile(models.Model):
    #this field is required
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='profile', )
    phone = models.CharField(
        null=True,
        blank=True,
        max_length=40, )
	register_date = models.DateField(
        auto_now_add=True,
        null=True, )
    delivery_area = models.OneToOneField(
        OrderDeliveryArea,
        on_delete=models.SET_NULL,
        max_length=150,
        null=True,
        blank=True, )
    delivery_city = models.OneToOneField(
        OrderDeliveryCity,
        on_delete=models.SET_NULL,
        max_length=150,
        null=True,
        blank=True, )
    delivery_address = models.CharField(
        max_length=150,
        null=True,
        blank=True, )
    activation_key = models.CharField(
        null=True,
        blank=True,
        max_length=240, )
    key_expires = models.DateTimeField(
        null=True,
        blank=True, )

    def __str__(self):
        return "Клиент %s" % self.user.username

    def user_email(self):
        return self.user.email

    def user_username(self):
        return self.user.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
