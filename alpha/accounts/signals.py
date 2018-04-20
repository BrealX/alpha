from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as User_
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from .models import Profile
from utils.decorators import disable_for_loaddata


User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		instance.profile = Profile.objects.create(user=instance)
	instance.profile.save()


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
	# when user changes his email his username is automatically changed if not in database
    email = email_address.email
    all_users = User_.objects.all()
    user = email_address.user
    usernames = [user.username for user in all_users]
    if not user.is_active:
        user.is_active = True
    if email not in usernames:
        user.username = email
    user.save()
