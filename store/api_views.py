import re
import json
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Product, Cart, CartItem, Wishlist, Category
from .views import get_or_create_cart


@require_POST
def api_cart_add(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return JsonResponse({'success': False, 'error': 'Product ID required'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)

    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        'success': True,
        'message': f'Added {product.name} to cart.',
        'cart_count': cart.total_items,
        'product': {
            'id': product.id,
            'name': product.name,
            'price': float(product.current_price),
            'image': product.main_image,
        }
    })


@require_POST
def api_cart_update(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    item_id = data.get('item_id')
    action = data.get('action', 'increase')

    try:
        item = CartItem.objects.select_related('cart', 'product').get(id=item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart item not found'}, status=404)

    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            item = None
    elif action == 'set':
        qty = int(data.get('quantity', 1))
        if qty > 0:
            item.quantity = qty
            item.save()
        else:
            item.delete()
            item = None

    cart = get_or_create_cart(request)

    return JsonResponse({
        'success': True,
        'cart_count': cart.total_items,
        'item_quantity': item.quantity if item else 0,
        'item_line_total': float(item.line_total) if item else 0.0,
        'subtotal': float(cart.subtotal),
        'savings': float(cart.total_savings),
        'delivery_charge': float(cart.delivery_charge),
        'final_total': float(cart.final_total),
    })


@require_POST
def api_cart_remove(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    item_id = data.get('item_id')
    try:
        item = CartItem.objects.get(id=item_id)
        cart = item.cart
        item.delete()
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

    return JsonResponse({
        'success': True,
        'cart_count': cart.total_items,
        'subtotal': float(cart.subtotal),
        'savings': float(cart.total_savings),
        'delivery_charge': float(cart.delivery_charge),
        'final_total': float(cart.final_total),
    })


@require_POST
def api_wishlist_toggle(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'login_required': True,
            'message': 'Please login to save items to your wishlist.'
        }, status=401)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    product_id = data.get('product_id')
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found'}, status=404)

    existing = Wishlist.objects.filter(user=request.user, product=product).first()
    if existing:
        existing.delete()
        added = False
        message = f'Removed {product.name} from wishlist.'
    else:
        Wishlist.objects.create(user=request.user, product=product)
        added = True
        message = f'Added {product.name} to wishlist.'

    count = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse({
        'success': True,
        'added': added,
        'wishlist_count': count,
        'message': message,
    })


@require_POST
def api_compare_toggle(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    product_id = int(data.get('product_id', 0))
    if not product_id:
        return JsonResponse({'success': False, 'error': 'Invalid product ID'}, status=400)

    compare_list = request.session.get('compare_list', [])
    if product_id in compare_list:
        compare_list.remove(product_id)
        in_compare = False
        msg = 'Product removed from comparison.'
    else:
        if len(compare_list) >= 3:
            return JsonResponse({
                'success': False,
                'error': 'You can compare up to 3 products at a time. Please remove one first.'
            }, status=400)
        compare_list.append(product_id)
        in_compare = True
        msg = 'Product added to comparison.'

    request.session['compare_list'] = compare_list
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'in_compare': in_compare,
        'compare_count': len(compare_list),
        'compare_ids': compare_list,
        'message': msg
    })


@require_GET
def api_search_suggest(request):
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__name__icontains=query) |
        Q(description__icontains=query)
    )[:6]

    results = []
    for p in products:
        results.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price),
            'current_price': float(p.current_price),
            'image': p.main_image,
            'category': p.category.name,
            'rating': p.rating,
        })

    return JsonResponse({'results': results})


@require_POST
def api_ai_assistant(request):
    """
    Intelligent shopping assistant endpoint.
    Parses budget, categories, specifications, and keywords from natural language prompts.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    prompt = data.get('prompt', '').strip()
    if not prompt:
        return JsonResponse({'success': False, 'error': 'Prompt is required'}, status=400)

    # 1. Budget extraction
    budget = None
    budget_match = re.search(r'(?:under|below|less than|within|around|upto|up to|budget|sub)\s*(?:rs\.?|inr|₹)?\s*(\d+[\d,]*)', prompt, re.IGNORECASE)
    if not budget_match:
        budget_match = re.search(r'(?:₹|rs\.?)\s*(\d+[\d,]*)', prompt, re.IGNORECASE)

    if budget_match:
        try:
            budget = float(budget_match.group(1).replace(',', ''))
        except ValueError:
            budget = None

    # 2. Extract Category and keywords
    lower_prompt = prompt.lower()
    cat_keywords = {
        'Electronics': ['headphone', 'headphones', 'earphone', 'laptop', 'macbook', 'keyboard', 'monitor', 'display', 'mouse', 'audio', 'sound', 'tech', 'gadget'],
        'Fashion': ['jacket', 'hoodie', 'shoes', 'chinos', 'shirt', 'clothing', 'wear', 'jeans', 'sneaker', 'pants', 'apparel', 'outfit'],
        'Beauty': ['serum', 'skincare', 'skin', 'face', 'oil', 'cream', 'moisturizer', 'glow', 'beauty'],
        'Home & Living': ['diffuser', 'chair', 'desk', 'aroma', 'home', 'living', 'furniture', 'decor', 'lamp', 'vase'],
        'Accessories': ['watch', 'smartwatch', 'sunglasses', 'wallet', 'glasses', 'leather', 'titanium', 'accessory'],
        'Sports': ['running', 'dumbbell', 'dumbbells', 'weights', 'gym', 'fitness', 'workout', 'yoga', 'sport', 'exercise', 'training']
    }

    matched_categories = []
    for cat_name, words in cat_keywords.items():
        if any(w in lower_prompt for w in words):
            matched_categories.append(cat_name)

    # 3. Intent & attribute tags
    attributes = ['wireless', 'bluetooth', 'noise cancelling', 'gaming', 'ergonomic', 'leather', 'cotton', 'waterproof', 'minimalist', 'running', 'casual']
    matched_attrs = [attr for attr in attributes if attr in lower_prompt]

    # Query DB
    q_filter = Q()
    if matched_categories:
        q_filter &= Q(category__name__in=matched_categories)

    if matched_attrs:
        attr_filter = Q()
        for attr in matched_attrs:
            attr_filter |= Q(name__icontains=attr) | Q(description__icontains=attr) | Q(specifications__icontains=attr)
        q_filter &= attr_filter

    # Also check other words in prompt
    ignore_words = {'i', 'need', 'a', 'an', 'the', 'for', 'under', 'in', 'to', 'and', 'or', 'with', 'best', 'good', 'cheap', 'buy', 'looking', 'show', 'me', 'want'}
    tokens = [w for w in re.findall(r'\b\w+\b', lower_prompt) if len(w) > 2 and w not in ignore_words and not w.isdigit()]

    # First attempt: category + attributes
    results = Product.objects.filter(q_filter)

    # If too narrow or empty, try token search across all products
    if results.count() == 0 and tokens:
        token_q = Q()
        for t in tokens:
            token_q |= Q(name__icontains=t) | Q(description__icontains=t) | Q(category__name__icontains=t)
        results = Product.objects.filter(token_q)

    # Fallback to top featured if still empty
    if results.count() == 0:
        results = Product.objects.filter(is_featured=True)

    # Filter by budget if extracted
    if budget:
        budget_filtered = results.filter(Q(discount_price__lte=budget) | Q(discount_price__isnull=True, price__lte=budget))
        if budget_filtered.exists():
            results = budget_filtered

    # Order by rating and discount
    matched_products = list(results.order_by('-rating', '-reviews_count')[:4])

    # Craft dynamic AI explanation
    summary_parts = []
    if matched_categories:
        summary_parts.append(f"in **{', '.join(matched_categories)}**")
    if matched_attrs:
        summary_parts.append(f"featuring **{', '.join(matched_attrs)}**")
    if budget:
        summary_parts.append(f"within your budget of **₹{budget:,.0f}**")

    if summary_parts:
        criteria_text = " " + " and ".join(summary_parts)
    else:
        criteria_text = f" matching '{prompt}'"

    reply_text = f"I analyzed your request and found {len(matched_products)} top-rated recommendation{'s' if len(matched_products) != 1 else ''}{criteria_text}. Here are the best choices tailored for you:"


    product_cards = []
    for p in matched_products:
        product_cards.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price),
            'current_price': float(p.current_price),
            'discount_percentage': p.discount_percentage,
            'rating': p.rating,
            'reviews_count': p.reviews_count,
            'image': p.main_image,
            'category': p.category.name,
            'in_stock': p.is_in_stock,
            'detail_url': f'/product/{p.slug}/',
        })

    return JsonResponse({
        'success': True,
        'message': reply_text,
        'budget': budget,
        'matched_categories': matched_categories,
        'products': product_cards
    })
