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
        initial='Ваше имя'
    )
    anonymous_email = forms.EmailField(
        required=True,
        label='Ваш email',
        initial='Ваш email'
    )
    anonymous_phone = forms.CharField(
        required=True,
        label='Контактный номер телефона',
        initial='Номер телефона'
    )

    
class CheckoutFormRight(forms.Form):
    anonymous_area = forms.ChoiceField()
    anonymous_city = forms.ChoiceField(
        #queryset=City.objects.all(),
        required=True,
        label='Город',
        widget=Select2Widget,
        #widget=ModelSelect2Widget(
        #    model=City,
        #    search_fields=['name__icontains'],
        #    dependent_fields={'area': 'area'},
        #    max_results=500,
        #)
        #choices={'1': 'Australia', '2': 'USA'}
    )
    anonymous_additional = forms.CharField(
        required=False,
        label='Дополнительная информация: укажите номер и адрес отделения склада перевозчика или Ваш полный почтовый адрес (не требуется заполнять при самовывозе)',
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(CheckoutFormRight, self).__init__(*args, **kwargs)
        self.fields['anonymous_area'] = forms.ChoiceField(
            choices=([("", "--- Выберите область ---")] + [(i['Ref'], i['Description']) for i in AREAS_LIST]),
            required=True,
            label='Область',
            initial='Выберите область',
            widget=Select2Widget)


def get_areas():
    '''
    Gets Areas list from Nova Poshta API 
    https://api.novaposhta.ua/v2.0/{format}/ [json]
    '''
    # Sending request for Areas
    url = 'https://api.novaposhta.ua/v2.0/json/Address/getAreas'
    headers = {'Content-Type': 'application/json'}
    context = {
        'apiKey': config('NOVA_POSHTA_API_KEY'),
        "modelName": "Address",
        "calledMethod": "getAreas",
        "methodProperties": {}
    }
    context = json.dumps(context, separators=(',', ':'))
    answer = requests.post(url, headers=headers, data=context)
    
    # Getting responce with data
    data = answer.json()
    # If response code is 200 --> save data
    if answer.status_code == requests.codes.ok:
        if data['success'] == True:
            context = {
                'errors': data['errors'],
                'warnings': data['warnings'],
                'info': data['info'],
                'areas': [{'Ref': area['Ref'], 'Description': area['Description']} for area in data['data']]
            }
        return context['areas']

AREAS_LIST = get_areas()