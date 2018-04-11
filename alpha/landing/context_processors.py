from products.models import Product, ProductCategory, ProductImage


def navigation_bar(request):
    nav_products_microphones = Product.objects.filter(is_active=True, category__id=1)
    nav_products_players = Product.objects.filter(is_active=True, category__id=2)
    nav_categories = ProductCategory.objects.filter(is_active=True)
    all_products = Product.objects.filter(is_active=True)
    new_arrivals = all_products.order_by('-created')
    for product in new_arrivals:
        pass
    user = request.user
    if user.is_authenticated:
        if user.first_name:
            username = user.first_name
        else:
            username = user.username
    return locals()
