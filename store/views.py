import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    Category, Product, ProductImage, Cart, CartItem,
    Order, OrderItem, Wishlist, Review, UserAddress
)

def get_or_create_cart(request):
    """Helper to retrieve or initialize user/session cart."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        session_key = request.session.session_key
        if session_key:
            session_cart = Cart.objects.filter(session_key=session_key).first()
            if session_cart and session_cart != cart:
                for item in session_cart.items.all():
                    user_item, created = CartItem.objects.get_or_create(
                        cart=cart, product=item.product,
                        defaults={'quantity': item.quantity}
                    )
                    if not created:
                        user_item.quantity += item.quantity
                        user_item.save()
                session_cart.delete()
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart


def home_view(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True)[:8]
    trending_products = Product.objects.filter(is_trending=True)[:8]
    flash_deals = Product.objects.filter(is_flash_deal=True)[:4]
    showcase_product = Product.objects.filter(is_featured=True).first()

    recent_ids = request.session.get('recently_viewed', [])
    recently_viewed = []
    if recent_ids:
        product_map = {p.id: p for p in Product.objects.filter(id__in=recent_ids)}
        recently_viewed = [product_map[pid] for pid in recent_ids if pid in product_map]

    deal_deadline = timezone.now() + timezone.timedelta(hours=14, minutes=32, seconds=45)

    user_wishlist_ids = set()
    if request.user.is_authenticated:
        user_wishlist_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'trending_products': trending_products,
        'flash_deals': flash_deals,
        'showcase_product': showcase_product,
        'recently_viewed': recently_viewed,
        'deal_deadline': deal_deadline.isoformat(),
        'user_wishlist_ids': user_wishlist_ids,
    }
    return render(request, 'store/home.html', context)


def product_list_view(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    selected_category = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    min_rating = request.GET.get('rating', '').strip()
    in_stock_only = request.GET.get('in_stock', '').strip()
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'popular').strip()

    if selected_category:
        products = products.filter(category__slug=selected_category)

    if query:
        search_terms = query.split()
        for term in search_terms:
            products = products.filter(
                Q(name__icontains=term) |
                Q(description__icontains=term) |
                Q(category__name__icontains=term) |
                Q(specifications__icontains=term)
            )

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    if in_stock_only == '1':
        products = products.filter(stock__gt=0)

    if sort_by == 'price_low':
        products = products.order_by('discount_price', 'price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-rating', '-reviews_count')

    user_wishlist_ids = set()
    if request.user.is_authenticated:
        user_wishlist_ids = set(Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True))

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'in_stock_only': in_stock_only,
        'query': query,
        'sort_by': sort_by,
        'total_count': products.count(),
        'user_wishlist_ids': user_wishlist_ids,
    }
    return render(request, 'store/product_list.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    reviews = product.reviews.all()

    recent = request.session.get('recently_viewed', [])
    if product.id in recent:
        recent.remove(product.id)
    recent.insert(0, product.id)
    request.session['recently_viewed'] = recent[:8]
    request.session.modified = True

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()
        if comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=max(1, min(5, rating)),
                title=title or 'Verified Purchase Review',
                comment=comment
            )
            all_reviews = product.reviews.all()
            product.reviews_count = all_reviews.count()
            product.rating = round(all_reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0, 1)
            product.save()
            messages.success(request, 'Thank you! Your review has been published.')
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/product_detail.html', context)


def cart_view(request):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'items': cart.items.select_related('product').all(),
    }
    return render(request, 'store/cart.html', context)


def checkout_view(request):
    cart = get_or_create_cart(request)
    if cart.total_items == 0:
        messages.warning(request, 'Your cart is empty. Add products before checkout.')
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        payment_method = request.POST.get('payment_method', 'UPI')

        if not (name and email and phone and address and city and pincode):
            messages.error(request, 'Please complete all required shipping fields.')
            return render(request, 'store/checkout.html', {'cart': cart, 'items': cart.items.all()})

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer_name=name,
            email=email,
            phone=phone,
            shipping_address=address,
            city=city,
            state=state,
            pincode=pincode,
            payment_method=payment_method,
            payment_status='Completed' if payment_method != 'COD' else 'Pending',
            order_status='Placed',
            subtotal=cart.subtotal,
            discount_amount=cart.total_savings,
            delivery_charge=cart.delivery_charge,
            total_amount=cart.final_total,
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_image=item.product.main_image,
                price=item.product.current_price,
                quantity=item.quantity
            )
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
                item.product.save()

        if request.user.is_authenticated and request.POST.get('save_address'):
            UserAddress.objects.get_or_create(
                user=request.user,
                full_name=name,
                phone=phone,
                address_line=address,
                city=city,
                state=state,
                pincode=pincode
            )

        cart.items.all().delete()
        request.session['last_order_id'] = order.order_id

        messages.success(request, f'Order #{order.order_id} placed successfully!')
        return redirect('order_confirmation', order_id=order.order_id)

    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'name': f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
            'email': request.user.email,
        }
        saved_addr = UserAddress.objects.filter(user=request.user).first()
        if saved_addr:
            initial_data.update({
                'phone': saved_addr.phone,
                'address': saved_addr.address_line,
                'city': saved_addr.city,
                'state': saved_addr.state,
                'pincode': saved_addr.pincode,
            })

    context = {
        'cart': cart,
        'items': cart.items.select_related('product').all(),
        'initial': initial_data,
    }
    return render(request, 'store/checkout.html', context)


def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})


def order_tracking_view(request, order_id=None):
    order = None
    query_id = request.GET.get('order_id', order_id or '').strip()
    if query_id:
        order = Order.objects.filter(order_id__iexact=query_id).first()
        if not order:
            messages.error(request, f'No order found with ID "{query_id}". Please check and try again.')

    return render(request, 'store/order_tracking.html', {
        'order': order,
        'searched_id': query_id
    })


@login_required
def profile_view(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    saved_addresses = UserAddress.objects.filter(user=request.user)

    context = {
        'orders': user_orders,
        'wishlist_items': wishlist_items,
        'addresses': saved_addresses,
    }
    return render(request, 'store/profile.html', context)


@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


def compare_view(request):
    compare_ids = request.session.get('compare_list', [])
    products = Product.objects.filter(id__in=compare_ids)
    return render(request, 'store/compare.html', {
        'products': products,
        'compare_ids': compare_ids
    })


# Authentication Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not (name and email and username and password):
            messages.error(request, 'All fields are required.')
            return render(request, 'store/auth/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/auth/register.html')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'store/auth/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return render(request, 'store/auth/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'store/auth/register.html')

        parts = name.split(None, 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        login(request, user)
        messages.success(request, f'Welcome to NEXORA, {first_name}!')
        return redirect('home')

    return render(request, 'store/auth/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = None
        if '@' in username_or_email:
            matched = User.objects.filter(email=username_or_email).first()
            if matched:
                user = authenticate(request, username=matched.username, password=password)
        else:
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'store/auth/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out safely.')
    return redirect('home')
