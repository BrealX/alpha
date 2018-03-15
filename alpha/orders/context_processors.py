from .models import ProductInBasket


def getting_cart_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    products_in_cart = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_in_cart_total_qnty = products_in_cart.count()

    return locals()