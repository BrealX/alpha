from django import forms
from .models import *


class CheckoutFormLeft(forms.Form):
    anonymous_name = forms.CharField(
        required=True,
        label='Ваше имя',
    )
    anonymous_email = forms.EmailField(
        required=True,
        label='Ваш email',
    )
    anonymous_phone = forms.CharField(
        required=True,
        label='Контактный номер телефона',
    )

    
class CheckoutFormRight(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(CheckoutFormRight, self).__init__(*args, **kwargs)
        areas_list = OrderDeliveryArea.objects.all()
        cities_list = OrderDeliveryCity.objects.all()
        initial_area = 'Выберите область'
        initial_city = 'Выберите город'
        self.fields['anonymous_area'] = forms.ChoiceField(
            choices=[('', '-- Выберите область --')] + [(area.id, area.name) for area in areas_list],
            required=True,
            label='Область',
            initial=initial_area,
            )
        self.fields['anonymous_city'] = forms.ChoiceField(
            choices=[('', '-- Выберите город --')] + [(city.id, city.name) for city in cities_list],
            required=True,
            label='Город',
            initial=initial_city,
            )
        self.fields['anonymous_additional'] = forms.CharField(
            required=False,
            label='Дополнительная информация: укажите номер и адрес отделения склада перевозчика или Ваш полный почтовый адрес (не требуется заполнять при самовывозе)',
            widget=forms.Textarea,
            initial='Введите адрес'
            )
