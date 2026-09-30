from .models import Category, Cart, Wishlist

def global_store_context(request):
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0
    compare_list = request.session.get('compare_list', [])

    # Cart count calculation
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_count = cart.total_items
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
            if cart:
                cart_count = cart.total_items

    return {
        'global_categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'compare_count': len(compare_list),
        'compare_list': compare_list,
    }
