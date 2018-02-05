from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import CheckoutContactForm
from django.contrib.auth.models import User


def add_to_cart(request):
    return_dict = dict()
    session_key = request.session.session_key
    product_id = request.POST.get('product_id')
    qnty = request.POST.get('qnty')
    is_delete = request.POST.get('is_delete')

    if is_delete == 'true':
        print('Is delete = true')
        deleted_items = ProductInBasket.objects.filter(session_key=session_key, id=product_id).update(is_active=False)
        print(deleted_items)
    else:
        print('Is delete = false')
        new_product_in_basket, created = ProductInBasket.objects.get_or_create(
            session_key=session_key, product_id=product_id, is_active=True, defaults={'qnty': qnty})
        if not created:
            new_product_in_basket.qnty += int(qnty)
            new_product_in_basket.save(force_update=True)

    products_in_cart = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_in_cart_total_qnty = products_in_cart.count()

    return_dict['products_in_cart_total_qnty'] = products_in_cart_total_qnty
    return_dict['products'] = list()
    for item in products_in_cart:
        product_dict = dict()
        product_dict['id'] = item.product.id
        product_dict['name'] = item.product.name
        product_dict['price_per_item'] = item.price_per_item
        product_dict['qnty'] = item.qnty
        product_dict['image'] = item.product.product_main_image.image.url
        product_dict['total_price'] = item.total_price
        return_dict['products'].append(product_dict)
    print(return_dict)
    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)

    #form = CheckoutContactForm(request.POST or None)
    #if request.POST:
        #if form.is_valid():
            #data = request.POST
            #name = data.get('name')
            #phone = data.get('phone')
            #user, created = User.objects.get_or_create(username=phone, defaults={'first_name': name})
            
            #order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

    #for name, value in data.items():
    #    if name.startswith('product_in_basket_'):
    #        product_in_basket_id = name.split('product_in_basket_')[1]
    #        product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
    #        product_in_basket.nmb = value
    #        product_in_basket.order = order
    #        product_in_basket.save(force_update=True)
    #        ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb, price_per_item=product_in_basket.price_per_item, total_price=product_in_basket.total_price, order=order)
    #    else:
    #        print('no')
    return render(request, 'orders/checkout.html', locals())