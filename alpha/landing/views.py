from django.shortcuts import render
from products.models import Product


def home(request):
    user = request.user
    return render(request, 'landing/home.html', locals())
