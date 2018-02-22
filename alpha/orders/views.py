from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import CheckoutFormLeft, CheckoutFormRight, AREAS_LIST
from django.contrib.auth.models import User
from decouple import config
import requests
import json


def add_to_cart(request):
    return_dict = dict()
    session_key = request.session.session_key
    product_in_cart_id = request.POST.get('product_id')
    qnty = request.POST.get('qnty')
    is_delete = request.POST.get('is_delete')

    if is_delete == 'true':
        items_to_delete = ProductInBasket.objects.get(session_key=session_key, id=product_in_cart_id)
        items_to_delete.is_active = False
        items_to_delete.save(force_update=True)
    else:
        new_product_in_basket, created = ProductInBasket.objects.get_or_create(
            session_key=session_key, product_id=product_in_cart_id, is_active=True, defaults={'qnty': qnty})
        if not created:
            new_product_in_basket.qnty += int(qnty)
            new_product_in_basket.save(force_update=True)

    products_in_cart = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_in_cart_total_qnty = products_in_cart.count()

    return_dict['products_in_cart_total_qnty'] = products_in_cart_total_qnty
    return_dict['products'] = list()
    for item in products_in_cart:
        product_dict = dict()
        product_dict['id'] = item.id
        product_dict['name'] = item.product.name
        product_dict['price_per_item'] = item.price_per_item
        product_dict['qnty'] = item.qnty
        product_dict['image'] = item.product.product_main_image.image.url
        product_dict['total_price'] = item.total_price
        return_dict['products'].append(product_dict)
    return JsonResponse(return_dict)


def auth(request):
    return render(request, 'orders/auth.html', locals())


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)

    return render(request, 'orders/checkout.html', locals())


def checkout1(request):
    user = request.user
    if request.POST:
        data = request.POST
        form1 = CheckoutFormLeft(request.POST or None)
        form2 = CheckoutFormRight(request.POST or None)
        if form1.is_valid():
            cd1 = form1.cleaned_data
            #cd2 = form2.cleaned_data
            new_order = Order.objects.create(
                customer_name=cd1['anonymous_name'],
                customer_email=cd1['anonymous_email'],
                customer_phone=cd1['anonymous_phone'],
                customer_address=str(data.get('anonymous_area', 'None')) + ', ' + str(data.get('anonymous_city', 'None')) + ', ' + str(data.get('anonymous_additional', 'None')),
                status=Status.objects.get(id=1),
                is_active=False
                )
            return redirect('checkout2', order_id=new_order.id)
        print(form1.errors, form2.errors)
    form1 = CheckoutFormLeft()
    form2 = CheckoutFormRight()
    return render(request, 'orders/checkout1.html', locals())


def checkout2(request, order_id):
    order_id = order_id
    return render(request, 'orders/checkout2.html', locals())


def get_cities(request):
    #Gets Cities list from Delivery Auto API 
    # Sending request for Cities
    area_id = request.GET.get('area_id', None)
    if str(area_id) in [str(area['id']) for area in AREAS_LIST]:
        url = 'http://www.delivery-auto.com/api/v4/Public/GetAreasList?culture=%s&regionId=%s&country=%s' % ('ru-RU', area_id, '1')
        headers = {'Content-Type': 'application/json'}
        answer = requests.get(url, headers=headers)
        # Getting responce with data
        data = answer.json()
        # If response code is 200 --> save data
        if answer.status_code == requests.codes.ok:
            if data['status'] == True:
                context = {
                    'cities': [{city['id']: city['name']} for city in data['data']]}
                if data['data']:
                    return JsonResponse(dict(cities=context['cities']))
                return JsonResponse({'error': 'No data returned'})
            else:
                context = {'errors': data['message']}
                return JsonResponse(context['errors'])
    print('No such area')
    return JsonResponse({'error': 'Error. No such region'})




'''def get_cities(request):
    Gets Cities list from Nova Poshta API 
    https://api.novaposhta.ua/v2.0/{format}/ [json]
    # Sending request for Cities
    id_area = request.GET.get('id_area', None)
    if id_area in [city['Ref'] for city in AREAS_LIST]:
        url = 'https://api.novaposhta.ua/v2.0/json/AddressGeneral/getSettlements'
        headers = {'Content-Type': 'application/json'}
        context = {
            "modelName": "AddressGeneral",
            "calledMethod": "getSettlements",
            "methodProperties": {
                "Area": 'dcaadb64-4b33-11e4-ab6d-005056801329',
                "Page": 1,
                "Warehouse": 1
            },
            "apiKey": config('NOVA_POSHTA_API_KEY')
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
                    'cities': [{city['Ref']: city['Description']} for city in data['data']]
                }
                if data['data']:
                    return JsonResponse(dict(cities=context['cities']))
                return JsonResponse({'error': 'No data returned'})
            else:
                context = {'errors': data['errors']}
                return JsonResponse(context['errors'])
    return JsonResponse({'error': 'Error. No such region'})'''