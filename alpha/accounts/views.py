# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.models import User
from .models import Profile
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail


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
					return HttpResponseRedirect(reverse('checkout1'))
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
		reg_form = UserRegistrationForm()
	args['login_form'] = login_form
	args['reg_form'] = reg_form
	args['login_error'] = login_error
	args['reg_error'] = reg_error
	return render(request, 'accounts/auth.html', args)


def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')


@login_required(login_url='/auth/login')
def user_cabinet(request):
	return locals()


#@login_required(login_url='/auth/login')
def after_registration(request):
	# Successful account registration alert & activation link creation
	user = User.objects.latest('id')
	#User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
	profile = user.profile
	print(profile)
	profile.activation_link = request.COOKIES['sessionid']
	profile.save()

	# Email settings
	subject = 'Активация аккаунта на сайте "Книжный Ёж"'
	activation_link = '{{ site }}/activation/%s' % request.COOKIES['sessionid']
	message = 'Дорогой посетитель, для активации Вашей учетной записи воспользуйтесь ссылкой: \
		%s \
		Спасибо за регистрацию! Удачных Вам покупок!' % activation_link
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


def account_activation(request, activation_id):
	# New account activation from emailed activation link
	profiles_count = Profile.objects.filter(activation_link__exact=activation_id).count()
	if profiles_count == 0:
		return Http404

	profiles = Profile.objects.filter(activation_link__exact=activation_id)[:1]
	for profile in profiles:
		profile.is_active = True
		profile.save()
	args = {}
	args['message'] = message
	return render(request, 'account_activation.html', args)

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
