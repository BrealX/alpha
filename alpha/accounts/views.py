# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserAddPersonalForm
from orders.forms import CheckoutFormRight
from django.contrib.auth.models import User
from .models import Profile
from orders.models import OrderDeliveryArea, OrderDeliveryCity, Order, OrderItem
from products.models import Review
from products.forms import ReviewForm
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
import datetime
import hashlib
import os
import binascii
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


''' hack to make Django Allauth Set Password working.

Initially when loggin in or signing up with social account user has no password. 
He should set it manually. This view doesn't work properly because user gets a default
non usable password with value '!' by Django. The User model's save() method is overriden 
and it checks if the password is usable. If it isn't, it means that a staff member has 
changed it and it must be hashed calling make_password() Django function. So as a result
the user signed up via social account has already usable password (hashed '!').
Then when Allauth SetPassword View checks if user has usable_password (allauth views.py line 597)
it redirects the User to ChangePassword View, where he should change the password that he doesn't
know actually.

To fix this, I have added some code to the standard Django User model.
So: at django.contrib.auth.models

add line 'from django.contrib.auth.hashers import is_password_usable, make_password' to the top
then add:

def save(self, *args, **kwargs):
    if self.password != '!' and not is_password_usable(self.password):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

to the class User(AbstractUser) (line 357 Django 2.0.3)

After that fix Allauth Set password View works correctly.
https://github.com/pennersr/django-allauth/issues/373'''



def user_login(request):
    args = {}
    args.update(csrf(request))
    login_error = None
    if request.POST:
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['user_email'].lower()
            user = authenticate(username=username, password=cd['user_password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    login_error = 'Данный аккаунт заблокирован. Пожалуйста, свяжитесь с нами для' \
                        + ' восстановления учетной записи!'
            else:
                login_error = 'Пользователь с таким email не зарегистрирован либо введен неверный пароль. Пожалуйста,' \
                    + ' проверьте введенные данные!'
    else:
        login_form = LoginForm()
    args['login_form'] = login_form
    args['login_error'] = login_error
    return render(request, 'accounts/auth.html', args)


def user_register(request):
    args = {}
    args.update(csrf(request))
    reg_error = ''
    if request.POST:
        reg_form = UserRegistrationForm(request.POST or None)
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
        reg_form = UserRegistrationForm(request.POST or None)
    args['reg_form'] = reg_form
    args['reg_error'] = reg_error
    return render(request, 'accounts/register.html', args)


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='account_login')
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html', locals())


@login_required(login_url='account_login')
def user_my_profile(request):
    user = request.user
    return render(request, 'accounts/user_my_profile.html', locals())


@login_required(login_url='account_login')
def user_my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_active=True).order_by('-created')
    return render(request, 'accounts/user_my_orders.html', locals())


@login_required(login_url='account_login')
def user_order_info(request, order_id):
    user = request.user
    order = Order.objects.get(id=order_id, user=user, is_active=True)
    order_items = OrderItem.objects.filter(order=order, is_active=True)
    return render(request, 'accounts/user_order_info.html', locals())


@login_required(login_url='account_login')
def user_my_reviews(request):
    user = request.user
    feedbacks = Review.objects.filter(user=user, is_active=True).order_by('-created')
    form = ReviewForm(request.POST or None)
    if request.POST and form.is_valid():
        review_product_id = request.POST.get('product_id')
        review_text = request.POST.get('text')
        review_score = int(request.POST.get('score'))
        review = Review.objects.get(user=user, product_id=review_product_id)
        review, created = Review.objects.update_or_create(
            user=user, 
            product_id=review_product_id,
            defaults={'text': review_text, 'score': review_score}) 
    return render(request, 'accounts/user_my_reviews.html', locals())


@login_required(login_url='account_login')
def add_address(request):
    user = request.user
    form = CheckoutFormRight(user)
    message = ""
    if request.POST:
        form = CheckoutFormRight(user, request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user.profile.delivery_area = OrderDeliveryArea.objects.get(id=cd['anonymous_area'])
            user.profile.delivery_city = OrderDeliveryCity.objects.get(id=cd['anonymous_city'])
            user.profile.delivery_address = str(cd['anonymous_additional'])
            user.save()
            return redirect('user_my_profile')  
        else:
            message = "Вы пытаетесь отправить пустую форму. Пожалуйста, заполните " + \
                "поля формы."    
    return render(request, 'accounts/user_add_address.html', locals())


@login_required(login_url='account_login')
def delete_address(request):
    user = request.user
    user.profile.delivery_area = None
    user.profile.delivery_city = None
    user.profile.delivery_address = None
    user.save()
    return_dict = {}
    return_dict['profile_delivery_city'] = user.profile.delivery_city
    return JsonResponse(return_dict)


@login_required(login_url='account_login')
def add_personal(request):
    user = request.user
    message_error = ""
    message_success = ""
    if request.POST:
        form = UserAddPersonalForm(request.POST or None)
        if form.is_valid():
            data = request.POST
            profile_phone = data.get('profile_phone')
            user_firstname = data.get('user_firstname')
            user.profile.phone = profile_phone
            user.first_name = user_firstname
            user.save()
            message_success = "Данные успешно изменены. Спасибо!"
            return render(request, 'accounts/user_add_personal.html', locals())  
        else:
            message_error = "Вы пытаетесь отправить пустую форму, либо заполнили не все поля."    
    form = UserAddPersonalForm()
    return render(request, 'accounts/user_add_personal.html', locals())


@login_required(login_url='account_login')
def delete_personal(request):
    user = request.user
    user.first_name = ''
    user.profile.phone = ''
    user.save()
    return_dict = {}
    return_dict['user_firstname'] = user.first_name
    return_dict['profile_phone'] = user.profile.phone
    return JsonResponse(return_dict)


@login_required(login_url='account_login')
def delete_account(request):
    '''makes current User inactive and marks his username as deleted in order to
    user can create his profile again with the same username later if needed'''
    return_dict = {}
    if request.POST:
        user = request.user
        if user.is_superuser:
            pass
        else:
            User.objects.filter(id=user.id).update(email=user.username)
            name = 'zzdeleted' + str(user.id)
            process = User.objects.filter(id=user.id).update(is_active=False, username=name)
    return JsonResponse(return_dict)


def after_registration(request):
    # Successful account registration alert & activation link creation
    user = User.objects.latest('id')
    salt = binascii.hexlify(os.urandom(32))
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
