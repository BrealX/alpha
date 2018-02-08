from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
	if request.POST:
		form = LoginForm(request.POST or None)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'], password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Авторизация прошла успешно')
				else:
					return HttpResponse('Аккаунт заблокирован')
			else:
				return HttpResponse('Неверный логин')
	else:
		form = LoginForm()
	return render(request, 'accounts/login.html', {'form': form})



#form = CheckoutContactForm(request.POST or None)
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
