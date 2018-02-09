from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User


def user_login(request):
	error = None
	if request.POST:
		login_form = LoginForm(request.POST or None)
		if login_form.is_valid():
			cd = login_form.cleaned_data
			user = authenticate(email=cd['user_email'], password=cd['user_password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('checkout1'))
				elif not(user.is_active):
					error = 'Данный аккаунт заблокирован. Пожалуйста, свяжитесь с нами для' \
						+ ' восстановления учетной записи!'
			else:
				error = 'Пользователь с таким email не зарегистрирован. Пожалуйста,' \
					+ ' проверьте введенные данные или зарегистрируйтесь!'
	else:
		login_form = LoginForm()
	return render(request, 'accounts/auth.html', {'login_form': login_form, 'error': error})




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
