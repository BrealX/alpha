from carton.cart import Cart


def getting_cart_info(request):
    cart = Cart(request.session)

    return locals()
