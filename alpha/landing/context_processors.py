from products.models import Product, ProductCategory, ProductImage


def navigation_bar(request):
    nav_products_microphones = Product.objects.filter(is_active=True, category__id=1)
    nav_products_players = Product.objects.filter(is_active=True, category__id=2)
    nav_categories = ProductCategory.objects.filter(is_active=True)
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images_microphones = products_images.filter(product__category__id=1)
    products_images_players = products_images.filter(product__category__id=2)
    user = request.user
    if user.is_authenticated:
        if user.first_name:
            username = user.first_name
        else:
            username = user.username
    return locals()
    