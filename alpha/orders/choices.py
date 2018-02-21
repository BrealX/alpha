from decouple import config
import requests
import json


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
                'areas': [i['Description'] for i in data['data']],
            }
        states = sorted(context['areas'])
        states = [{'id': index, 'area': value} for (index, value) in enumerate(states)]
        return states


STATE_CHOICES = get_areas()