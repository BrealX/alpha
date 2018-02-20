# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserAddAddressForm, UserAddPersonalForm
from django.contrib.auth.models import User
from .models import Profile
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
import datetime, hashlib, os
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


def user_login(request):
    args = {}
    args.update(csrf(request))
    login_error = None
    reg_error = None
    if request.POST:
        login_form = LoginForm(request.POST or None)
        reg_form = UserRegistrationForm(request.POST or None)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['user_email'].lower()
            user = authenticate(username=username, password=cd['user_password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('checkout1')
                else:
                    login_error = 'Данный аккаунт заблокирован. Пожалуйста, свяжитесь с нами для' \
                        + ' восстановления учетной записи!'
            else:
                login_error = 'Пользователь с таким email не зарегистрирован либо введен неверный пароль. Пожалуйста,' \
                    + ' проверьте введенные данные!'
        if reg_form.is_valid():
            try:
                data = request.POST
                new_user_email = data.get('new_user_email')
                new_user_name = data.get('new_user_name')
                new_user, created = User.objects.get_or_create(
                    username=new_user_email, 
                    first_name=new_user_name,
                    email=new_user_email,
                    is_active=False
                )
                new_user.set_password(reg_form.cleaned_data['password'])
                new_user.save()
                return render(request, 'registration/register_done.html', {'new_user': new_user})
            except Exception:
                reg_error = 'Пользователь с таким email уже зарегистрирован. Попробуйте другой адрес.'
    else:
        login_form = LoginForm()
        reg_form = UserRegistrationForm(request.POST or None)
    args['login_form'] = login_form
    args['reg_form'] = reg_form
    args['login_error'] = login_error
    args['reg_error'] = reg_error
    return render(request, 'accounts/auth.html', args)


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/auth/login')
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html', locals())


@login_required(login_url='/auth/login')
def user_my_profile(request):
    user = request.user
    return render(request, 'accounts/user_my_profile.html', locals())   


@login_required(login_url='/auth/login')
def add_address(request):
    user = request.user
    message = ""
    if request.POST:
        form = UserAddAddressForm(request.POST or None)
        if form.is_valid():
            data = request.POST
            if data.get('profile_delivery_address'):
                profile_delivery_address = data.get('profile_delivery_address')
                user.profile.delivery_address = profile_delivery_address
                user.save()
                message = "Данные успешно изменены. Спасибо!"
            return render(request, 'accounts/user_add_address.html', locals())  
        else:
            message = "Вы пытаетесь отправить пустую форму. Пожалуйста, заполните " + \
                "поля формы."    
    form = UserAddAddressForm()
    return render(request, 'accounts/user_add_address.html', locals())


@login_required(login_url='/auth/login')
def delete_address(request):
    user = request.user
    user.profile.delivery_address = None
    user.save()
    return_dict = {}
    return_dict['profile_delivery_address'] = user.profile.delivery_address
    return JsonResponse(return_dict)


@login_required(login_url='/auth/login')
def add_personal(request):
    user = request.user
    message = ""
    if request.POST:
        form = UserAddPersonalForm(request.POST or None)
        if form.is_valid():
            data = request.POST
            profile_phone = data.get('profile_phone')
            user_firstname = data.get('user_firstname')
            user.profile.phone = profile_phone
            user.first_name = user_firstname
            user.save()
            message = "Данные успешно изменены. Спасибо!"
            return render(request, 'accounts/user_add_personal.html', locals())  
        else:
            message = "Вы пытаетесь отправить пустую форму. Пожалуйста, заполните " + \
                "поля формы."    
    form = UserAddPersonalForm()
    return render(request, 'accounts/user_add_personal.html', locals())


@login_required(login_url='/auth/login')
def delete_personal(request):
    user = request.user
    user.first_name = ''
    user.profile.phone = ''
    user.save()
    print(user.first_name)
    print(user.profile.phone)
    return_dict = {}
    return_dict['user_firstname'] = user.first_name
    return_dict['profile_phone'] = user.profile.phone
    return JsonResponse(return_dict)


@login_required(login_url='/auth/login')
def delete_account(request):
    '''makes current User inactive and marks his username as deleted in order to
    user can create his profile again with the same username later if needed'''
    if request.POST:
        user = request.user
        User.objects.filter(id=user.id).update(email=user.username)
        name = 'zzdeleted' + str(user.id)
        process = User.objects.filter(id=user.id).update(is_active=False, username=name)
        return_dict = {}
    return JsonResponse(return_dict)


def after_registration(request):
    # Successful account registration alert & activation link creation
    user = User.objects.latest('id')
    salt = os.urandom(32).hex()
    activation_key = hashlib.sha512()
    activation_key.update(('%s%s' % (salt, user.username)).encode('utf-8'))
    activation_key = activation_key.hexdigest()
    key_expires = datetime.datetime.today() + datetime.timedelta(2)
    user.profile.activation_key = activation_key
    user.profile.key_expires = key_expires
    user.save()

    # Email settings
    subject = 'Активация аккаунта на сайте "Книжный Ёж"'
    message = render_to_string(
        template_name='registration/acc_active_email.html', 
        context={
        'user': user, 
        'domain': get_current_site(request), 
        'activation_key': activation_key
        })

    send_to = user.email

    send_mail(
        subject, 
        message, 
        settings.EMAIL_HOST_USER, 
        [send_to], 
        fail_silently=False)    

    args = {}
    args['user'] = user
    return render(request, 'registration/after_registration.html', args)


def account_activation(request, activation_key):
    # New account activation from emailed activation link
    user_profile = get_object_or_404(Profile, activation_key=activation_key)
    error = None
    if user_profile.key_expires < timezone.now():
        error = 1
        return render(request, 'registration/account_activation.html', {'error': error})
    user_account = user_profile.user
    user_account.is_active = True
    user_profile.activation_key = ""
    user_account.save()
    return render(request, 'registration/account_activation.html')

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
