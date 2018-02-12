# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required


def user_login(request):
	args = {}
	args.update(csrf(request))
	error = None
	if request.POST:
		login_form = LoginForm(request.POST or None)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			username = cd['user_email'].lower()
			user = authenticate(username=username, password=cd['user_password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('checkout1'))
				else:
					error = 'Данный аккаунт заблокирован. Пожалуйста, свяжитесь с нами для' \
						+ ' восстановления учетной записи!'
			else:
				error = 'Пользователь с таким email не зарегистрирован либо введен неверный пароль. Пожалуйста,' \
					+ ' проверьте введенные данные!'
	else:
		login_form = LoginForm()
	args['login_form'] = login_form
	args['error'] = error
	return render(request, 'accounts/auth.html', args)


def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')


@login_required(login_url='/auth/login')
def user_cabinet(request):
	return locals()


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
