from django.shortcuts import render
from products.models import Product
from decouple import config
import re
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from alpha.settings import DEFAULT_FROM_EMAIL


def home(request):
    user = request.user
    return render(request, 'landing/home.html', locals())


def contacts(request):
    user = request.user
    shop_tel = config('SHOP_TEL')
    shop_email = config('SHOP_EMAIL')
    return render(request, 'landing/contacts.html', locals())		


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
