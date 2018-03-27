from carton.cart import Cart


def getting_cart_info(request):
    product_cart = Cart(request.session)

    return locals()
