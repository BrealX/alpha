from django.forms import ModelForm
from .models import *


class SubscriberForm(ModelForm):

	class Meta:
		model = Subscriber
		#fields = [""]
		exclude = [""]