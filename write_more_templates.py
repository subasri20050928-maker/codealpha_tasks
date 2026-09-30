import os

t_detail = """{% extends 'store/base.html' %}
{% block title %}{{ product.name }} | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:3.5rem 1.5rem;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:3.5rem;align-items:start;">
    <div>
      <div style="border-radius:var(--radius-md);overflow:hidden;background:var(--bg-surface);border:1px solid var(--border-subtle);height:460px;">
        <img src="{{ product.main_image }}" alt="{{ product.name }}" style="width:100%;height:100%;object-fit:cover;">
      </div>
    </div>
    <div>
      <div class="product-category-tag">{{ product.category.name }}</div>
      <h1 style="font-size:2.4rem;font-weight:800;margin-bottom:1rem;line-height:1.2;">{{ product.name }}</h1>
      <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;">
        <div class="product-rating">★ {{ product.rating }} ({{ product.reviews_count }} reviews)</div>
        <span style="color:var(--success);font-weight:700;">✓ In Stock</span>
      </div>
      <div style="display:flex;align-items:baseline;gap:1rem;margin-bottom:1.5rem;">
        <span class="current-price" style="font-size:2.2rem;">₹{{ product.current_price }}</span>
        {% if product.has_discount %}
        <span class="original-price" style="font-size:1.2rem;">₹{{ product.price }}</span>
        <span class="discount-badge" style="position:static;">Save {{ product.discount_percentage }}%</span>
        {% endif %}
      </div>
      <p style="color:var(--text-muted);font-size:1.05rem;line-height:1.7;margin-bottom:2rem;">{{ product.description }}</p>
      <div style="display:flex;gap:1rem;align-items:center;margin-bottom:2rem;">
        <input type="number" id="detailQty" value="1" min="1" max="10" class="form-control" style="width:70px;text-align:center;">
        <button onclick="addToCart({{ product.id }}, parseInt(document.getElementById('detailQty').value), this)" class="btn btn-primary" style="padding:0.85rem 2rem;">Add to Cart 🛒</button>
        <button onclick="toggleWishlist({{ product.id }}, this)" class="btn btn-secondary">❤️ Wishlist</button>
      </div>
    </div>
  </div>
</div>
{% endblock %}
"""

t_cart = """{% extends 'store/base.html' %}
{% block title %}Cart | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:3.5rem 1.5rem;">
  <h1 style="font-size:2.2rem;font-weight:800;margin-bottom:2rem;">Shopping Cart</h1>
  {% if items %}
  <div style="display:grid;grid-template-columns:1.8fr 1fr;gap:2.5rem;align-items:start;">
    <div class="table-card">
      <table class="table">
        <thead><tr><th>Product</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr></thead>
        <tbody>
          {% for item in items %}
          <tr>
            <td style="display:flex;align-items:center;gap:1rem;">
              <img src="{{ item.product.main_image }}" style="width:55px;height:55px;border-radius:var(--radius-sm);object-fit:cover;">
              <div>
                <a href="{% url 'product_detail' item.product.slug %}" style="font-weight:700;">{{ item.product.name }}</a>
              </div>
            </td>
            <td>₹{{ item.product.current_price }}</td>
            <td>
              <button onclick="updateCartItem({{ item.id }}, 'decrease')" class="btn btn-secondary btn-sm" style="padding:0.2rem 0.6rem;">-</button>
              <span style="font-weight:700;padding:0 0.5rem;">{{ item.quantity }}</span>
              <button onclick="updateCartItem({{ item.id }}, 'increase')" class="btn btn-secondary btn-sm" style="padding:0.2rem 0.6rem;">+</button>
            </td>
            <td style="font-weight:700;color:var(--primary);">₹{{ item.line_total }}</td>
            <td><button onclick="removeCartItem({{ item.id }})" style="background:none;border:none;color:var(--danger);cursor:pointer;font-size:1.1rem;">✕</button></td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:2rem;">
      <h3 style="font-size:1.25rem;font-weight:700;margin-bottom:1.5rem;">Order Summary</h3>
      <div style="display:flex;justify-content:space-between;margin-bottom:0.75rem;"><span>Subtotal</span><span>₹{{ cart.subtotal }}</span></div>
      {% if cart.total_savings > 0 %}<div style="display:flex;justify-content:space-between;margin-bottom:0.75rem;color:var(--success);"><span>Discounts</span><span>-₹{{ cart.total_savings }}</span></div>{% endif %}
      <div style="display:flex;justify-content:space-between;margin-bottom:1rem;"><span>Delivery</span><span>{% if cart.delivery_charge == 0 %}FREE{% else %}₹{{ cart.delivery_charge }}{% endif %}</span></div>
      <div style="border-top:1px solid var(--border-subtle);padding-top:1rem;display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1.5rem;">
        <span style="font-weight:700;font-size:1.1rem;">Total</span>
        <span style="font-size:1.8rem;font-weight:800;color:var(--accent);">₹{{ cart.final_total }}</span>
      </div>
      <a href="{% url 'checkout' %}" class="btn btn-primary btn-block" style="padding:0.9rem;">Proceed to Checkout 💳</a>
    </div>
  </div>
  {% else %}
  <div style="text-align:center;padding:4rem 2rem;background:var(--bg-card);border-radius:var(--radius-md);">
    <h2>Your cart is empty</h2>
    <p style="color:var(--text-muted);margin:1rem 0 1.5rem;">Discover our trending products.</p>
    <a href="{% url 'product_list' %}" class="btn btn-primary">Start Shopping</a>
  </div>
  {% endif %}
</div>
{% endblock %}
"""

t_checkout = """{% extends 'store/base.html' %}
{% block title %}Checkout | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:3.5rem 1.5rem;max-width:900px;">
  <h1 style="font-size:2.2rem;font-weight:800;margin-bottom:2rem;">Complete Your Order</h1>
  <form method="POST" style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:2rem;">
    {% csrf_token %}
    <h3 style="margin-bottom:1.25rem;">1. Shipping Details</h3>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
      <div class="form-group"><label class="form-label">Full Name</label><input type="text" name="name" value="{{ initial.name|default:'' }}" required class="form-control" placeholder="John Doe"></div>
      <div class="form-group"><label class="form-label">Phone</label><input type="text" name="phone" value="{{ initial.phone|default:'' }}" required class="form-control" placeholder="+91 98765 43210"></div>
    </div>
    <div class="form-group"><label class="form-label">Email</label><input type="email" name="email" value="{{ initial.email|default:'' }}" required class="form-control" placeholder="john@example.com"></div>
    <div class="form-group"><label class="form-label">Address</label><textarea name="address" rows="2" required class="form-control">{{ initial.address|default:'' }}</textarea></div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;">
      <div class="form-group"><label class="form-label">City</label><input type="text" name="city" value="{{ initial.city|default:'' }}" required class="form-control"></div>
      <div class="form-group"><label class="form-label">State</label><input type="text" name="state" value="{{ initial.state|default:'' }}" required class="form-control"></div>
      <div class="form-group"><label class="form-label">Pincode</label><input type="text" name="pincode" value="{{ initial.pincode|default:'' }}" required class="form-control"></div>
    </div>
    <h3 style="margin:2rem 0 1rem;">2. Payment Method</h3>
    <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:2rem;">
      <label style="padding:1rem;background:var(--bg-surface);border:1px solid var(--border-accent);border-radius:var(--radius-sm);cursor:pointer;flex:1;">
        <input type="radio" name="payment_method" value="UPI" checked> Instant UPI / QR
      </label>
      <label style="padding:1rem;background:var(--bg-surface);border:1px solid var(--border-subtle);border-radius:var(--radius-sm);cursor:pointer;flex:1;">
        <input type="radio" name="payment_method" value="Card"> Credit / Debit Card
      </label>
      <label style="padding:1rem;background:var(--bg-surface);border:1px solid var(--border-subtle);border-radius:var(--radius-sm);cursor:pointer;flex:1;">
        <input type="radio" name="payment_method" value="COD"> Cash on Delivery
      </label>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:1.5rem;">
      <span style="font-size:1.2rem;font-weight:700;">Final Amount:</span>
      <span style="font-size:2rem;font-weight:800;color:var(--accent);">₹{{ cart.final_total }}</span>
    </div>
    <button type="submit" class="btn btn-primary btn-block" style="padding:1rem;">Place Order Now →</button>
  </form>
</div>
{% endblock %}
"""

t_conf = """{% extends 'store/base.html' %}
{% block title %}Order Confirmed | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:4rem 1.5rem;max-width:800px;text-align:center;">
  <div style="width:70px;height:70px;border-radius:var(--radius-full);background:rgba(16,185,129,0.2);color:var(--success);font-size:2.2rem;display:inline-flex;align-items:center;justify-content:center;margin-bottom:1.5rem;">✓</div>
  <h1 style="font-size:2.4rem;font-weight:800;">Order Confirmed!</h1>
  <p style="color:var(--text-muted);font-size:1.1rem;margin-bottom:1rem;">Thank you, {{ order.customer_name }}! Your order has been placed.</p>
  <div style="display:inline-block;padding:0.4rem 1.25rem;background:var(--bg-surface);border:1px solid var(--border-accent);border-radius:var(--radius-full);font-weight:700;margin-bottom:2.5rem;">
    Order ID: <span style="color:var(--primary);">{{ order.order_id }}</span>
  </div>

  <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-lg);padding:2.5rem;margin-bottom:2.5rem;text-align:left;">
    <h3 style="font-size:1.15rem;font-weight:700;margin-bottom:1rem;">Order Status Timeline</h3>
    <div class="timeline-track">
      <div class="timeline-progress-bar" style="width:15%;"></div>
      <div class="timeline-step completed"><div class="timeline-node">1</div><div class="timeline-label">Placed</div></div>
      <div class="timeline-step"><div class="timeline-node">2</div><div class="timeline-label">Confirmed</div></div>
      <div class="timeline-step"><div class="timeline-node">3</div><div class="timeline-label">Packed</div></div>
      <div class="timeline-step"><div class="timeline-node">4</div><div class="timeline-label">Shipped</div></div>
      <div class="timeline-step"><div class="timeline-node">5</div><div class="timeline-label">Delivered</div></div>
    </div>
    <div style="text-align:center;color:var(--accent);font-weight:700;margin-top:1.5rem;">Current Status: {{ order.get_order_status_display }}</div>
  </div>

  <div style="display:flex;gap:1rem;justify-content:center;">
    <a href="{% url 'home' %}" class="btn btn-primary">Continue Shopping</a>
    <a href="{% url 'order_tracking_detail' order.order_id %}" class="btn btn-secondary">Track Order 📍</a>
  </div>
</div>
{% endblock %}
"""

t_track = """{% extends 'store/base.html' %}
{% block title %}Track Order | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:4rem 1.5rem;max-width:800px;">
  <h1 style="font-size:2.2rem;font-weight:800;margin-bottom:1.5rem;text-align:center;">Track Your Order</h1>
  <form method="GET" style="display:flex;gap:0.75rem;margin-bottom:2.5rem;">
    <input type="text" name="order_id" value="{{ searched_id }}" required class="form-control" placeholder="Enter Order ID e.g. NX-892415">
    <button type="submit" class="btn btn-primary">Track</button>
  </form>

  {% if order %}
  <div style="background:var(--bg-card);border:1px solid var(--border-accent);border-radius:var(--radius-lg);padding:2.5rem;">
    <div style="display:flex;justify-content:space-between;margin-bottom:2rem;">
      <div>
        <h3>Order #{{ order.order_id }}</h3>
        <div style="color:var(--text-dim);font-size:0.85rem;">{{ order.customer_name }} - {{ order.created_at|date:"M d, Y" }}</div>
      </div>
      <span style="color:var(--primary);font-weight:800;">{{ order.get_order_status_display }}</span>
    </div>

    <div class="timeline-track">
      <div class="timeline-progress-bar" style="width:{% if order.order_status == 'Placed' %}15%{% elif order.order_status == 'Confirmed' %}38%{% elif order.order_status == 'Packed' %}62%{% elif order.order_status == 'Shipped' %}85%{% elif order.order_status == 'Delivered' %}100%{% else %}0%{% endif %};"></div>
      <div class="timeline-step {% if order.status_step_index >= 1 %}completed{% endif %}"><div class="timeline-node">1</div><div class="timeline-label">Placed</div></div>
      <div class="timeline-step {% if order.status_step_index >= 2 %}completed{% endif %}"><div class="timeline-node">2</div><div class="timeline-label">Confirmed</div></div>
      <div class="timeline-step {% if order.status_step_index >= 3 %}completed{% endif %}"><div class="timeline-node">3</div><div class="timeline-label">Packed</div></div>
      <div class="timeline-step {% if order.status_step_index >= 4 %}completed{% endif %}"><div class="timeline-node">4</div><div class="timeline-label">Shipped</div></div>
      <div class="timeline-step {% if order.status_step_index >= 5 %}completed{% endif %}"><div class="timeline-node">5</div><div class="timeline-label">Delivered</div></div>
    </div>
  </div>
  {% endif %}
</div>
{% endblock %}
"""

t_profile = """{% extends 'store/base.html' %}
{% block title %}Profile | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:3.5rem 1.5rem;">
  <h1 style="font-size:2.2rem;font-weight:800;margin-bottom:2rem;">My Account</h1>
  <div style="display:grid;grid-template-columns:1fr 2fr;gap:2.5rem;">
    <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:2rem;">
      <h3>{{ user.get_full_name|default:user.username }}</h3>
      <div style="color:var(--text-muted);font-size:0.9rem;margin-bottom:1.5rem;">{{ user.email }}</div>
      <a href="{% url 'logout' %}" class="btn btn-secondary btn-sm">Sign Out</a>
    </div>
    <div>
      <h3 style="font-size:1.4rem;font-weight:700;margin-bottom:1rem;">Recent Orders</h3>
      {% if orders %}
        {% for o in orders %}
        <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:1.25rem;margin-bottom:1rem;">
          <div style="display:flex;justify-content:space-between;margin-bottom:0.5rem;">
            <strong>Order #{{ o.order_id }}</strong>
            <span style="color:var(--primary);font-weight:700;">{{ o.get_order_status_display }}</span>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="color:var(--accent);font-weight:800;">₹{{ o.total_amount }}</span>
            <a href="{% url 'order_tracking_detail' o.order_id %}" class="btn btn-secondary btn-sm">Track 📍</a>
          </div>
        </div>
        {% endfor %}
      {% else %}
        <p style="color:var(--text-muted);">No past orders found.</p>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}
"""

t_wishlist = """{% extends 'store/base.html' %}
{% block title %}Wishlist | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:3.5rem 1.5rem;">
  <h1 style="font-size:2.2rem;font-weight:800;margin-bottom:2rem;">My Wishlist ❤️</h1>
  {% if wishlist_items %}
  <div class="product-grid">
    {% for item in wishlist_items %}
    <div class="product-card">
      <div class="product-thumb-wrap">
        <a href="{% url 'product_detail' item.product.slug %}">
          <img src="{{ item.product.main_image }}" class="product-thumb">
        </a>
      </div>
      <div class="product-content">
        <h4 class="product-name"><a href="{% url 'product_detail' item.product.slug %}">{{ item.product.name }}</a></h4>
        <div class="current-price" style="margin-bottom:1rem;">₹{{ item.product.current_price }}</div>
        <button onclick="addToCart({{ item.product.id }}, 1, this)" class="btn btn-primary btn-sm btn-block">Move to Cart 🛒</button>
      </div>
    </div>
    {% endfor %}
  </div>
  {% else %}
  <div style="text-align:center;padding:4rem 2rem;background:var(--bg-card);border-radius:var(--radius-md);">
    <h3>Your wishlist is empty</h3>
    <a href="{% url 'product_list' %}" class="btn btn-primary btn-sm" style="margin-top:1rem;">Browse Products</a>
  </div>
  {% endif %}
</div>
{% endblock %}
"""

t_compare = """{% extends 'store/base.html' %}
{% block title %}Compare | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:3.5rem 1.5rem;">
  <h1 style="font-size:2.2rem;font-weight:800;margin-bottom:2rem;">Product Comparison</h1>
  {% if products %}
  <div class="table-card">
    <table class="table">
      <thead>
        <tr><th>Feature</th>{% for p in products %}<th style="text-align:center;">{{ p.name }}</th>{% endfor %}</tr>
      </thead>
      <tbody>
        <tr><td>Price</td>{% for p in products %}<td style="text-align:center;font-weight:800;color:var(--accent);">₹{{ p.current_price }}</td>{% endfor %}</tr>
        <tr><td>Rating</td>{% for p in products %}<td style="text-align:center;">★ {{ p.rating }}</td>{% endfor %}</tr>
        <tr><td>Action</td>{% for p in products %}<td style="text-align:center;"><button onclick="addToCart({{ p.id }}, 1, this)" class="btn btn-primary btn-sm">Add to Cart</button></td>{% endfor %}</tr>
      </tbody>
    </table>
  </div>
  {% else %}
  <div style="text-align:center;padding:4rem 2rem;background:var(--bg-card);border-radius:var(--radius-md);">
    <h3>No products selected for comparison</h3>
  </div>
  {% endif %}
</div>
{% endblock %}
"""

t_login = """{% extends 'store/base.html' %}
{% block title %}Login | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:5rem 1.5rem;max-width:440px;">
  <div style="background:var(--bg-card);border:1px solid var(--border-accent);border-radius:var(--radius-lg);padding:2.5rem;">
    <h2 style="font-size:1.8rem;font-weight:800;margin-bottom:1.5rem;text-align:center;">Sign In to NEXORA</h2>
    <form method="POST">
      {% csrf_token %}
      <div class="form-group"><label class="form-label">Username</label><input type="text" name="username" required autofocus class="form-control"></div>
      <div class="form-group"><label class="form-label">Password</label><input type="password" name="password" required class="form-control"></div>
      <button type="submit" class="btn btn-primary btn-block" style="margin-top:1.5rem;">Sign In →</button>
    </form>
    <div style="text-align:center;margin-top:1.5rem;font-size:0.9rem;">
      Don't have an account? <a href="{% url 'register' %}" style="color:var(--primary);font-weight:700;">Register</a>
    </div>
    <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid var(--border-subtle);font-size:0.8rem;color:var(--text-dim);text-align:center;">
      Demo User: <strong>john_doe</strong> / <strong>password123</strong><br>
      Admin: <strong>admin</strong> / <strong>admin123</strong>
    </div>
  </div>
</div>
{% endblock %}
"""

t_register = """{% extends 'store/base.html' %}
{% block title %}Register | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:4rem 1.5rem;max-width:460px;">
  <div style="background:var(--bg-card);border:1px solid var(--border-accent);border-radius:var(--radius-lg);padding:2.5rem;">
    <h2 style="font-size:1.8rem;font-weight:800;margin-bottom:1.5rem;text-align:center;">Join NEXORA</h2>
    <form method="POST">
      {% csrf_token %}
      <div class="form-group"><label class="form-label">Full Name</label><input type="text" name="name" required class="form-control"></div>
      <div class="form-group"><label class="form-label">Username</label><input type="text" name="username" required class="form-control"></div>
      <div class="form-group"><label class="form-label">Email</label><input type="email" name="email" required class="form-control"></div>
      <div class="form-group"><label class="form-label">Password</label><input type="password" name="password" required class="form-control"></div>
      <div class="form-group"><label class="form-label">Confirm Password</label><input type="password" name="confirm_password" required class="form-control"></div>
      <button type="submit" class="btn btn-primary btn-block" style="margin-top:1.5rem;">Create Account →</button>
    </form>
    <div style="text-align:center;margin-top:1.5rem;font-size:0.9rem;">
      Already registered? <a href="{% url 'login' %}" style="color:var(--primary);font-weight:700;">Sign In</a>
    </div>
  </div>
</div>
{% endblock %}
"""

files = {
    "store/templates/store/product_detail.html": t_detail,
    "store/templates/store/cart.html": t_cart,
    "store/templates/store/checkout.html": t_checkout,
    "store/templates/store/order_confirmation.html": t_conf,
    "store/templates/store/order_tracking.html": t_track,
    "store/templates/store/profile.html": t_profile,
    "store/templates/store/wishlist.html": t_wishlist,
    "store/templates/store/compare.html": t_compare,
    "store/templates/store/auth/login.html": t_login,
    "store/templates/store/auth/register.html": t_register,
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("[OK] All remaining templates created successfully")
