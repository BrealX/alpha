from django import forms
from .models import *
from django_select2.forms import Select2Widget


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
    anonymous_area = forms.ChoiceField()
    anonymous_city = forms.ChoiceField()
    anonymous_additional = forms.CharField(
        required=False,
        label='Дополнительная информация: укажите номер и адрес отделения склада перевозчика или Ваш полный почтовый адрес (не требуется заполнять при самовывозе)',
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(CheckoutFormRight, self).__init__(*args, **kwargs)
        areas_list = OrderDeliveryArea.objects.all()
        cities_list = OrderDeliveryCity.objects.all()
        self.fields['anonymous_area'] = forms.ChoiceField(
            choices=[('', '-- Выберите область --')] + [(area.id, area.name) for area in areas_list],
            required=True,
            label='Область',
            initial='Выберите область',
            widget=Select2Widget)
        self.fields['anonymous_city'] = forms.ChoiceField(
            choices=[('', '-- Выберите город --')] + [(city.id, city.name) for city in cities_list],
            required=True,
            label='Область',
            initial='Выберите город',
            widget=Select2Widget)