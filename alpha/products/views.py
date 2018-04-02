from django.shortcuts import render
from products.models import Product, Review
from orders.models import Order, OrderItem
from products.forms import ReviewForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
import re
from alpha.settings import DEFAULT_FROM_EMAIL
from decouple import config


def product_land(request, product_id):
    product = Product.objects.get(id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    user = request.user
    shop_email = config('SHOP_EMAIL')
    shop_tel = config('SHOP_TEL')
    product_order_times = Order.objects.filter(orderitem__product__id=product.id).count()  # how many times this product was ordered
    if product_order_times <= 100:
        product_order_times += 100
    happy_clients = Order.objects.filter(is_active=True).count()
    if happy_clients <= 300:
        happy_clients += 300
    form = ReviewForm(request.POST or None)
    feedbacks = Review.objects.filter(is_active=True, product=product).order_by('created')

    if user.is_authenticated:
        user_ordered_products = OrderItem.objects.filter(order__user=user, order__is_active=True, is_active=True, order__status__id=4)
        user_product_reviews = feedbacks.filter(user=user)
        if product in user_ordered_products:
            product_is_purchased = True
        if request.POST and form.is_valid():
            review_text = request.POST.get('text')
            review_score = int(request.POST.get('score'))
            new_form = form.save(commit=False)
            new_form.product = product
            new_form.user = user
            new_form.text = review_text
            new_form.score = review_score
            if user_ordered_products:
                new_form.order = user_ordered_products.last().order
            new_form.save()
    return render(request, 'products/product_landing.html', locals())


def contact(request):
    # Receives Ajax from Landing Page Contact Form and validates email field
    # Then if OK sends a message from user to site owners 
    contact_name = request.POST.get('contact_name', 'Инкогнито')
    contact_email = request.POST.get('contact_email', '')
    form_content = request.POST.get('form_content', 'Никакой вопрос не был задан')
    return_dict = dict()
    if contact_email:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", contact_email):
            return_dict['error'] = "Похоже, Вы ввели недопустимый адрес email!"
            return JsonResponse(return_dict)
        # Email settings
        subject = 'Новый вопрос на сайте "ЁжиК."'
        message = render_to_string(
            template_name='products/contact_form.html', 
            context={
                'contact_name': contact_name, 
                'contact_email': contact_email, 
                'form_content': form_content,
            })
        send_to = DEFAULT_FROM_EMAIL
        send_mail(
            subject, # Subject here
            message, # Mail message here
            contact_email, # Send From 
            [send_to], # Send To
            fail_silently=False,
        )
        return_dict['success'] = "Сообщение успешно отправлено! Мы постараемся ответить как можно скорее!"
        return JsonResponse(return_dict)
    return_dict['error'] = "Поле email не должно быть пустым"
    return JsonResponse(return_dict)
    