from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import CheckoutFormLeft, CheckoutFormRight
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import json

from carton.cart import Cart
from products.models import Product
from django.views.decorators.http import require_POST


@require_POST
def add_to_cart(request):
    cart = Cart(request.session)
    data = json.loads(request.POST.get('cart_changes'))
    for k, v in data.items():
        product = Product.objects.get(id=int(k))
        quantity = int(v['qnty'])
        is_delete = v['is_delete']
        if is_delete == 'true':
            cart.remove(product)
        else:
            if product in cart:
                cart.set_quantity(product, quantity=quantity)
            else:
                cart.add(product, price=product.price_with_discount(), quantity=quantity)

    products_in_cart = cart.items
    products_in_cart_total_qnty = cart.unique_count  

    return_dict = dict()
    return_dict['products_in_cart_total_qnty'] = products_in_cart_total_qnty
    return_dict['products_in_cart'] = list()
    for item in products_in_cart:
        product_dict = dict()
        product_dict['id'] = item.product.id
        product_dict['name'] = item.product.name
        product_dict['price'] = item.product.price_with_discount()
        product_dict['qnty'] = item.quantity
        product_dict['image'] = item.product.product_main_image.image.url
        product_dict['total_price'] = item.subtotal
        return_dict['products_in_cart'].append(product_dict)
    return JsonResponse(return_dict)


def auth(request):
    return render(request, 'orders/auth.html', locals())


def checkout(request):
    cart = Cart(request.session)
    cart_items = cart.items
    return render(request, 'orders/checkout.html', locals())


def checkout1(request):
    cart = Cart(request.session)
    cart_items = cart.items
    session_key = request.session.session_key
    user = request.user
    if cart.is_empty:
        message = 'Ваша корзина пуста. Для оформления заказа необходимо что-то в неё добавить'
        form1 = CheckoutFormLeft()
        form2 = CheckoutFormRight(request.user)
        return render(request, 'orders/checkout1.html', locals())
    else:
        if request.POST:
            # if request is POST
            data = request.POST
            form1 = CheckoutFormLeft(request.POST or None)
            form2 = CheckoutFormRight(request.user, request.POST or None)
            if form1.is_valid() and form2.is_valid():
                # if both forms are valid
                cd1 = form1.cleaned_data
                cd2 = form2.cleaned_data
                if user.is_authenticated:
                    # order creation for identified User
                    customer_address = str(OrderDeliveryArea.objects.get(id=cd2['anonymous_area'])) + ', ' + str(OrderDeliveryCity.objects.get(id=cd2['anonymous_city'])) + ', ' + str(cd2['anonymous_additional'])
                    new_order = Order.objects.create(
                        session_key=session_key,
                        user=user,
                        customer_name=data.get('anonymous_name', ''),
                        customer_email=data.get('anonymous_email', ''),
                        customer_phone=data.get('anonymous_phone', ''),
                        customer_address=customer_address,
                        status_id=1,
                        is_active=False
                    )
                    request.session['delivery_address'] = customer_address
                    return redirect('checkout2')
                else:
                    # order creation for anonymous User
                    customer_address = str(OrderDeliveryArea.objects.get(id=cd2['anonymous_area'])) + ', ' + str(OrderDeliveryCity.objects.get(id=cd2['anonymous_city'])) + ', ' + str(cd2['anonymous_additional'])
                    new_order = Order.objects.create(
                        session_key=session_key,
                        customer_name=cd1['anonymous_name'],
                        customer_email=cd1['anonymous_email'],
                        customer_phone=cd1['anonymous_phone'],
                        customer_address=customer_address,
                        status_id=1,
                        is_active=False
                        )
                    request.session['delivery_address'] = customer_address
                    return redirect('checkout2')
            else:
                # both forms are not valid or one of them is not
                message1 = form1.errors
                message2 =  form2.errors
                return render(request, 'orders/checkout1.html', locals())
        else:
            # if request is GET
            form1 = CheckoutFormLeft()
            if user.is_authenticated and user.profile.delivery_city:
                form2 = CheckoutFormRight(request.user, initial={'anonymous_area': user.profile.delivery_area.id, 'anonymous_city': user.profile.delivery_city.id, 'anonymous_additional': user.profile.delivery_address})
            else:
                form2 = CheckoutFormRight(request.user)
            return render(request, 'orders/checkout1.html', locals())


def checkout2(request):
    session_key = request.session.session_key
    user = request.user
    cart = Cart(request.session)
    cart_items = cart.items
    order_overall = cart.total
    order = Order.objects.filter(session_key=session_key).latest('id')
    delivery_address = request.session['delivery_address']
    return render(request, 'orders/checkout2.html', locals())


def get_chained_cities(request):
    # Receives area_id from AJAX and returns chained cities list from database
    area_id = request.GET.get('area_id', None)
    cities_list = OrderDeliveryCity.objects.filter(area_id=area_id)
    response_to_ajax = [{city.id: city.name} for city in cities_list]
    return JsonResponse(dict(cities=response_to_ajax))


def order_confirm(request):
    return_dict = dict()
    cart = Cart(request.session)
    order_id = int(request.GET.get('order_id', ''))
    order = Order.objects.get(id=order_id)
    order.is_active = True
    order.total_order_amount = cart.total
    order.save()
    return_dict['order_id'] = order.id
    return_dict['order_overall'] = order.total_order_amount
    return_dict['order_customer_email'] = order.customer_email
    return_dict['order_customer_name'] = order.customer_name
    cart = Cart(request.session)
    cart.clear()
    return JsonResponse(return_dict)


def order_notification(request):
    # Email settings
    data = request.GET
    subject = 'Новый заказ на сайте "ЁжиК."'
    message = render_to_string(
        template_name='orders/order_notification.html',
        context={
            'order_id': data.get('order_id', ''),
            'domain': get_current_site(request),
            'order_overall': data.get('order_overall', ''),
            'order_customer_name': data.get('order_customer_name'),
        })

    send_to = [data.get('order_customer_email'), settings.EMAIL_HOST_USER,]

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        send_to,
        fail_silently=False)

    return_dict = dict()
    return JsonResponse(return_dict)
