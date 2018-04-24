# -*- coding: utf-8 -*-
import datetime
import hashlib
import os
import binascii

from allauth.account.decorators import verified_email_required
from allauth.account.models import EmailAddress

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.template.context_processors import csrf
from django.utils import timezone

from .forms import LoginForm, UserRegistrationForm, UserChangeFirstnameForm, ProfileChangePhoneForm, ProfileChangeAddressForm, UserEmailChangeForm
from .models import Profile
from orders.models import OrderDeliveryArea, OrderDeliveryCity, Order, OrderItem
from products.models import Review
from products.forms import ReviewForm


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


# now using allauth login views, this view was written for backup
'''def user_login(request):
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
    return render(request, 'accounts/auth.html', args)'''


def user_logout(request):
    logout(request)
    return redirect('home')


@verified_email_required
@login_required(login_url='account_login')
def my_profile(request):
    return render(request, 'accounts/my_profile.html', locals())


@verified_email_required
@login_required(login_url='account_login')
def user_my_profile(request):
    user = request.user
    return render(request, 'accounts/user_my_profile.html', locals())


@verified_email_required
@login_required(login_url='account_login')
def user_my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user, is_active=True).order_by('-created')
    return render(request, 'accounts/user_my_orders.html', locals())


@verified_email_required
@login_required(login_url='account_login')
def user_order_info(request, order_id):
    user = request.user
    order = Order.objects.get(id=order_id, user=user, is_active=True)
    order_items = OrderItem.objects.filter(order=order, is_active=True)
    return render(request, 'accounts/user_order_info.html', locals())


@verified_email_required
@login_required(login_url='account_login')
def user_my_reviews(request):
    user = request.user
    feedbacks = Review.objects.filter(user=user, is_active=True).order_by('-created')
    form = ReviewForm(request.POST or None)
    if request.POST and form.is_valid():
        data = request.POST
        review_id = data.get('review_id')
        review_to_update = Review.objects.filter(
            user=user,
            is_active=True,
            id=review_id).update(
            text=data.get('text'),
            score=data.get('score'))
        messages.success(request, "Отзыв успешно изменён!")
    elif request.POST and not form.is_valid():
        messages.error(request, "Пожалуйста, устраните ошибки! Форма заполнена не верно!")
    return render(request, 'accounts/user_my_reviews.html', locals())


@verified_email_required
@login_required(login_url='account_login')
def add_address(request):
    user = request.user
    profile = user.profile
    form = ProfileChangeAddressForm(request.POST or None, instance=profile)
    if request.POST:
        if form.is_valid():
            data = request.POST
            profile_delivery_area_id = data.get('delivery_area')
            delivery_area = OrderDeliveryArea.objects.get(id=profile_delivery_area_id)
            profile_delivery_city_id = data.get('delivery_city')
            delivery_city = OrderDeliveryCity.objects.get(id=profile_delivery_city_id)
            profile_delivery_address = data.get('delivery_address')
            profile_to_change = form.save(commit=False)
            profile_to_change.delivery_area = delivery_area
            profile_to_change.delivery_city = delivery_city
            profile_to_change.delivery_address = profile_delivery_address
            profile_to_change.save()
            messages.success(request, "Адрес доставки успешно изменен!")
            return render(request, 'accounts/user_add_address.html', locals())
        else:
            messages.error(request, "Вы пытаетесь отправить пустую форму, либо заполнили не все поля!")
    return render(request, 'accounts/user_add_address.html', locals())


@verified_email_required
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


@verified_email_required
@login_required(login_url='account_login')
def add_personal(request):
    user = request.user
    user_form = UserChangeFirstnameForm(request.POST or None, instance=user)
    profile = user.profile
    profile_form = ProfileChangePhoneForm(request.POST or None, instance=profile)
    if request.POST:
        if user_form.is_valid() and profile_form.is_valid():
            data = request.POST
            profile_phone = data.get('phone')
            profile_to_change = profile_form.save(commit=False)
            profile_to_change.phone = profile_phone
            profile_to_change.save()

            user_firstname = data.get('first_name')
            user.profile.phone = profile_phone
            user_to_change = user_form.save(commit=False)
            user_to_change.first_name = user_firstname
            user_to_change.save()
            messages.success(request, "Персональные данные успешно изменены!")
            return render(request, 'accounts/user_add_personal.html', locals())
        else:
            messages.error(request, "Вы пытаетесь отправить пустую форму, либо заполнили не все поля!")
    return render(request, 'accounts/user_add_personal.html', locals())


@verified_email_required
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


@verified_email_required
@login_required(login_url='account_login')
def delete_review(request):
    user = request.user
    review_id = request.POST.get('feedback_id')
    review_to_delete = Review.objects.filter(
        user=user,
        is_active=True,
        id=review_id).update(
        is_active=False)
    return_dict = dict()
    messages.success(request, "Отзыв успешно удалён!")
    return JsonResponse(return_dict)


@verified_email_required
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
            email = user.email
            name = 'zzdeleted' + str(user.id)
            deleted_allauth_email = name + '@deleted.com'
            allauth_email = EmailAddress.objects.filter(user=user).update(email=deleted_allauth_email)
            process = User.objects.filter(id=user.id).update(is_active=False, username=name, email=name, last_name=email)
    return JsonResponse(return_dict)


@verified_email_required
@login_required(login_url='account_login')
def change_password(request):
    if request.POST:
        form = PasswordChangeForm(request.user, request.POST or None)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль был успешно обновлён!')
            return redirect('password_change')
        else:
            messages.error(request, 'Пожалуйста, устраните ошибки. Вы ввели неверный текущий пароль либо введенные новые пароли не совпадают. Также убедитесь, что все поля формы заполнены!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required(login_url='account_login')
def set_password(request):
    user = request.user
    form = SetPasswordForm(request.POST or None)
    if user.has_usable_password():
        return redirect('password_change')
    else:
        if request.POST:
            form = SetPasswordForm(user, request.POST or None)
            if form.is_valid():
                form.save(commit=True)
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль был успешно установлен!')
            else:
                messages.error(request, 'Пожалуйста, устраните ошибки. Введенные новые пароли не совпадают либо вы пытаетесь отправить пустую форму!')
    return render(request, 'accounts/set_password.html', locals())


@login_required(login_url='account_login')
def email_change(request):
    user = request.user
    form = UserEmailChangeForm(user, request.POST or None)
    if request.POST:
        if form.is_valid():
            new_email = request.POST.get('new_email1')
            allauth_email = EmailAddress.objects.get(user=user)
            allauth_email.change(request, new_email)
            messages.success(request, 'Электронный адрес успешно изменён!')
            return redirect('my_profile')
        messages.error(request, 'Форма заполнена не верно. Введенные адреса не совпадают либо не являются email адресами!')
        return render(request, 'accounts/change_email.html', locals())
    else:
        return render(request, 'accounts/change_email.html', locals())
