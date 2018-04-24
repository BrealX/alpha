from django.shortcuts import render, get_object_or_404
from django.views.generic import RedirectView

from orders.models import Order, OrderItem
from products.models import Product, Review
from products.forms import ReviewForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions


def product_land(request, product_id):
    product = Product.objects.get(id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    user = request.user
    product_order_times = Order.objects.filter(orderitem__product__id=product.id).count()  # how many times this product was ordered
    if product_order_times <= 100:
        product_order_times += 100
    happy_clients = Order.objects.filter(is_active=True).count()
    if happy_clients <= 300:
        happy_clients += 300
    form = ReviewForm(request.POST or None)
    feedbacks = Review.objects.filter(is_active=True, product=product).order_by('created')

    if user.is_authenticated:
        user_ordered_products = OrderItem.objects.filter(order__user=user, order__is_active=True, is_active=True, order__status__id=4)
        user_product_reviews = feedbacks.filter(user=user)
        if product in user_ordered_products:
            product_is_purchased = True
        if request.POST and form.is_valid():
            review_text = request.POST.get('text')
            review_score = int(request.POST.get('score'))
            new_form = form.save(commit=False)
            new_form.product = product
            new_form.user = user
            new_form.text = review_text
            new_form.score = review_score
            if user_ordered_products:
                new_form.order = user_ordered_products.last().order
            new_form.save()
    return render(request, 'products/product_landing.html', locals())


class ProductLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, product_id, format=None):
        obj = get_object_or_404(Product, id=product_id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False        
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        likes_count = obj.likes.count()
        data = {
            'updated': updated,
            'liked': liked,
            'likes_count': likes_count,
        }
        return Response(data)
