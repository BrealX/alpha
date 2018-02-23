#-*- coding: utf-8 -*-
from django.contrib.sessions.models import Session
from django.utils import timezone
from orders.models import ProductInBasket


sessions = Session.objects.filter(expire_date__gt=timezone.now())
for session in sessions:
    session = session.get_decoded()
    print(session)
    if '_auth_user_id' in session.keys():
        pass
    else:
        products_in_cart = ProductInBasket()

