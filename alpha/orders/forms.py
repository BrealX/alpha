from django import forms
from .models import *
from django_select2.forms import Select2Widget
from decouple import config
import requests
import json


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
    anonymous_city = forms.ChoiceField(
        #queryset=City.objects.all(),
        required=True,
        label='Город',
        widget=Select2Widget,
    )
    anonymous_additional = forms.CharField(
        required=False,
        label='Дополнительная информация: укажите номер и адрес отделения склада перевозчика или Ваш полный почтовый адрес (не требуется заполнять при самовывозе)',
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(CheckoutFormRight, self).__init__(*args, **kwargs)
        self.fields['anonymous_area'] = forms.ChoiceField(
            #choices=([("", "--- Выберите область ---")] + [(i['Ref'], i['Description']) for i in AREAS_LIST]),
            choices=[('', '-- Выберите область --')] + [(area['id'], area['name']) for area in AREAS_LIST],
            required=True,
            label='Область',
            initial='Выберите область',
            widget=Select2Widget)


def get_areas():
    '''
    Gets Areas list from Delivery Auto API 
    '''
    # Sending request for Areas
    url = 'http://www.delivery-auto.com/api/v4/Public/GetRegionList?culture=%s&country=%s' % ('ru-RU', '1')
    headers = {'Content-Type': 'application/json'}
    answer = requests.get(url, headers=headers)
    # Getting responce with data
    data = answer.json()
    # If response code is 200 --> save data
    if answer.status_code == requests.codes.ok:
        if data['status'] == True:
            context = {
                'errors': data['message'],
                'areas': [{'id': area['id'], 'name': area['name']} for area in data['data'][1:]]
            }
            return context['areas']


AREAS_LIST = get_areas()