from django import forms
from .models import *


class CheckoutFormLeft(forms.Form):
	anonymous_name = forms.CharField(
		required=True
	)
	anonymous_email = forms.EmailField(
		required=True
	)
	anonymous_phone = forms.CharField(
		required=True
	)

	
class CheckoutFormRight(forms.Form):
	anonymous_state = forms.ChoiceField(
		label='Область<sup>*</sup>',
		help_text='Выберите область',
		initial='Выберите область'
	)
	anonymous_region = forms.ChoiceField(
		label='Район<sup>*</sup>',
		help_text='Выберите район',
		initial='Выберите район',
	)
	anonymous_city = forms.ChoiceField(
		label='Населенный пункт<sup>*</sup>',
		help_text='Выберите населенный пункт',
		initial='Выберите населенный пункт',
	)
	anonymous_additional = forms.CharField(
		required=False,
		label='Дополнительная информация: <br>укажите номер и адрес отделения склада перевозчика или номер почтового отделения Укрпочты и адрес (не требуется заполнять при самовывозе)',
		widget=forms.Textarea,
	)
