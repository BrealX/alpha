from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from .forms import CheckoutFormLeft, CheckoutFormRight
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


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
    user = request.user
    products_in_cart = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    if not products_in_cart:
        message = "Ваша корзина пуста. Чтобы оформить заказ, необходимо добавить товар!"
    return render(request, 'orders/checkout.html', locals())


def checkout1(request):
    session_key = request.session.session_key
    user = request.user
    cart_products = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    if cart_products:
        if request.POST:
            data = request.POST
            form1 = CheckoutFormLeft(request.POST or None)
            form2 = CheckoutFormRight(request.POST or None)
            if form1.is_valid() and form2.is_valid():
                cd1 = form1.cleaned_data
                cd2 = form2.cleaned_data
                if cart_products:
                    if not user.is_authenticated:
                        new_order = Order.objects.create(
                            session_key=session_key,
                            customer_name=cd1['anonymous_name'],
                            customer_email=cd1['anonymous_email'],
                            customer_phone=cd1['anonymous_phone'],
                            customer_address=str(OrderDeliveryArea.objects.get(id=cd2['anonymous_area'])) + ', ' + str(OrderDeliveryCity.objects.get(id=cd2['anonymous_city'])) + ', ' + str(cd2['anonymous_additional']),
                            status_id=1,
                            is_active=False
                            )
                        for item in cart_products:
                            item.order = new_order
                            item.save(force_update=True)

                            ProductInOrder.objects.create(
                                session_key=session_key,
                                order=new_order,
                                product=item.product,
                                qnty=item.qnty,
                                price_per_item=item.price_per_item,
                                total_amount=item.total_price,
                                )
                        return redirect('checkout2')
                    else:
                        if user.profile.delivery_address:
                            customer_address = user.profile.delivery_address
                        customer_address = str(OrderDeliveryArea.objects.get(id=cd2['anonymous_area'])) + ', ' + str(
                                OrderDeliveryCity.objects.get(id=cd2['anonymous_city'])) + ', ' + str(
                                cd2['anonymous_additional'])
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
                        for item in cart_products:
                            item.order = new_order
                            item.save(force_update=True)

                            ProductInOrder.objects.create(
                                session_key=session_key,
                                order=new_order,
                                product=item.product,
                                qnty=item.qnty,
                                price_per_item=item.price_per_item,
                                total_amount=item.total_price,
                            )
                        return redirect('checkout2')
                else:
                    message = 'Ваша корзина пуста. Для оформления заказа необходимо что-то в неё добавить'
                    form1 = CheckoutFormLeft()
                    form2 = CheckoutFormRight()
                    return render(request, 'orders/checkout1.html', {'message': message, 'form1': form1, 'form2': form2 })
        form1 = CheckoutFormLeft()
        form2 = CheckoutFormRight()
        return render(request, 'orders/checkout1.html', locals())
    else:
        return redirect('checkout')


def checkout2(request):
    session_key = request.session.session_key
    products_in_cart = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__session_key=session_key)
    user = request.user
    order_overall = 0
    ordered_products = ProductInOrder.objects.filter(session_key=session_key, is_active=True)
    for order in ordered_products:
        order_overall += order.total_amount
        order = order.order
    delivery_address = ordered_products.latest('id').order.customer_address
    return render(request, 'orders/checkout2.html', locals())


def get_chained_cities(request):
    # Receives area_id from AJAX and returns chained cities list from database
    area_id = request.GET.get('area_id', None)
    cities_list = OrderDeliveryCity.objects.filter(area_id=area_id)
    response_to_ajax = [{city.id: city.name} for city in cities_list]
    return JsonResponse(dict(cities=response_to_ajax))


def order_confirm(request):
    return_dict = dict()
    order_id = int(request.GET.get('order_id', ''))
    order = Order.objects.filter(id=order_id)
    for item in order:
        item.is_active = True
        item.save()
        return_dict['order_id'] = item.id
        return_dict['order_status'] = item.status.name
        return_dict['order_overall'] = item.total_order_amount
        return_dict['order_customer_email'] = item.customer_email
        return_dict['order_customer_name'] = item.customer_name
    products_in_cart = ProductInBasket.objects.filter(order_id=order_id)
    for product in products_in_cart:
        product.is_active = False
        product.save()
    products_in_order = ProductInOrder.objects.filter(order_id=order_id)
    for prod_in_order in products_in_order:
        prod_in_order.is_active = False
        prod_in_order.save()
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
