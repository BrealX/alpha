from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .forms import UserCheckoutForm, ProfileCheckoutForm, AnonymousCheckoutForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import json
from carton.cart import Cart
from products.models import Product
from django.views.decorators.http import require_POST
from decouple import config
from django.urls import reverse


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
    if user.is_authenticated:
        profile = user.profile
        user_form = UserCheckoutForm(request.POST or None, instance=user)
        profile_form = ProfileCheckoutForm(request.POST or None, instance=profile)
    else:
        form = AnonymousCheckoutForm(request.POST or None)
    if cart.is_empty:
        message = 'Ваша корзина пуста. Для оформления заказа необходимо что-то в неё добавить'
        return render(request, 'orders/checkout1.html', locals())
    if request.POST:
        data = request.POST
        print(data)
        if user.is_authenticated:
            if user_form.is_valid() and profile_form.is_valid():
                order_area_id = data.get('delivery_area')
                order_area = OrderDeliveryArea.objects.get(id=order_area_id)
                order_city_id = data.get('delivery_city')
                order_city = OrderDeliveryCity.objects.get(id=order_city_id)
                order_address = data.get('delivery_address')
                order_full_address = str(order_area) + ', ' + str(order_city) + ', ' + str(order_address)
                new_order = Order.objects.create(
                    user=user,
                    customer_name=data.get('first_name'),
                    customer_email=data.get('email'),
                    customer_phone=data.get('phone'),
                    customer_address=order_full_address,
                    status_id=1,
                    is_active=False)
                for item in cart_items:
                    order_item = OrderItem.objects.create(
                        order=new_order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.price,
                        order_item_subtotal=item.subtotal)
                request.session['delivery_address'] = order_full_address
                return redirect('checkout2')
            else:  # if forms are not valid
                return render(request, 'orders/checkout1.html', locals())
        else:
            if form.is_valid():
                order_area_id = data.get('anonymous_area')
                order_area = OrderDeliveryArea.objects.get(id=order_area_id)
                order_city_id = data.get('anonymous_city')
                order_city = OrderDeliveryCity.objects.get(id=order_city_id)
                order_address = data.get('anonymous_additional')
                order_full_address = str(order_area) + ', ' + str(order_city) + ', ' + str(order_address)
                new_order = Order.objects.create(
                    session_key=session_key,
                    customer_name=data.get('anonymous_name'),
                    customer_email=data.get('anonymous_email'),
                    customer_phone=data.get('anonymous_phone'),
                    customer_address=order_full_address,
                    status_id=1,
                    is_active=False)
                for item in cart_items:
                    order_item = OrderItem.objects.create(
                        order=new_order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.price,
                        order_item_subtotal=item.subtotal)
                request.session['delivery_address'] = order_full_address
                return redirect('checkout2')
            else:  # if form is not valid
                return render(request, 'orders/checkout1.html', locals())
    return render(request, 'orders/checkout1.html', locals())


def checkout2(request):
    session_key = request.session.session_key
    user = request.user
    cart = Cart(request.session)
    cart_items = cart.items
    order_overall = cart.total
    if user.is_authenticated:
        order = Order.objects.filter(user=user, is_active=False).latest('id')
    else:
        order = Order.objects.filter(session_key=session_key).latest('id')
    order_id = order.id
    order_customer_phone = order.customer_phone
    order_customer_email = order.customer_email
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
    order_customer_name = data.get('order_customer_name', '')
    order_customer_email = data.get('order_customer_email', '')
    order_overall = data.get('order_overall', '')
    order_id = data.get('order_id', '')
    sitename = get_current_site(request)
    order = Order.objects.get(id=order_id, is_active=True)
    order_items = OrderItem.objects.filter(order_id=order_id, is_active=True)
    order_details = [('Товар: ' + str(item.product.name) + ', ' +
     'количество - ' + str(item.quantity) + ' шт., ' + 'по цене ' + str(item.price) + ' грн.') for item in order_items]
    order_delivery_address = order.customer_address
    order_customer_phone = order.customer_phone
    order_link = request.build_absolute_uri(reverse('user_my_orders'))
    
    subject = 'Новый заказ на сайте ' + str(sitename)
    message = render_to_string(
        template_name='orders/order_notification.txt')
    html_message_admin = render_to_string(
            'orders/order_notification_admin.html',
            context={
                'name': order_customer_name,
                'phone': order_customer_phone,
                'email': order_customer_email,
                'address': order_delivery_address,
                'sitename': sitename,
                'siteemail': config('DEFAULT_FROM_EMAIL'),
                'order_id': order_id,
                'order_overall': order_overall,
                'details': order_details,
            })
    html_message_user = render_to_string(
            'orders/order_notification_user.html',
            context={
                'email': order_customer_email,
                'sitename': sitename,
                'siteemail': config('DEFAULT_FROM_EMAIL'),
                'order_id': order_id,
                'order_overall': order_overall,
                'link': order_link,
            })

    # send notification to the site administration
    send_mail(
        subject=subject, # Subject here
        message=message, # Mail message here
        from_email=config('DEFAULT_FROM_EMAIL'), # Send From 
        recipient_list=[config('DEFAULT_FROM_EMAIL')], # Send To
        fail_silently=False,
        html_message=html_message_admin,
    )
    # send notification to the user
    send_mail(
        subject=subject, # Subject here
        message=message, # Mail message here
        from_email=config('DEFAULT_FROM_EMAIL'), # Send From 
        recipient_list=[order_customer_email, ], # Send To
        fail_silently=False,
        html_message=html_message_user,
    )

    return_dict = dict()
    return JsonResponse(return_dict)
