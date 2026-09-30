# write_html_templates.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. base.html
base_html = """{% load static %}
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}NEXORA | Smart Shopping, Simplified{% endblock %}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
  {% block extra_css %}{% endblock %}
</head>
<body>

  <!-- Navigation Bar -->
  <header class="navbar">
    <div class="container">
      <a href="{% url 'home' %}" class="brand-logo">
        <svg viewBox="0 0 24 24"><defs><linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#6366f1"/><stop offset="100%" stop-color="#ec4899"/></linearGradient></defs><polygon points="12 2 2 7 12 12 22 7 12 2"/><polygon points="2 17 12 22 22 17 12 12 2 17"/></svg>
        NEXORA
      </a>

      <ul class="nav-links">
        <li><a href="{% url 'home' %}" class="nav-link {% if request.resolver_match.url_name == 'home' %}active{% endif %}">Home</a></li>
        <li><a href="{% url 'product_list' %}" class="nav-link {% if request.resolver_match.url_name == 'product_list' and not request.GET.sort %}active{% endif %}">Shop</a></li>
        <li><a href="{% url 'product_list' %}#categories" class="nav-link">Categories</a></li>
        <li><a href="{% url 'product_list' %}?sort=popular" class="nav-link">Trending</a></li>
        <li><a href="{% url 'home' %}#flash-deals" class="nav-link">⚡ Deals</a></li>
      </ul>

      <!-- Smart Search -->
      <form action="{% url 'product_list' %}" method="GET" class="nav-search-box">
        <span class="nav-search-icon">🔍</span>
        <input type="text" name="q" value="{{ request.GET.q|default:'' }}" class="nav-search-input" placeholder="Search laptop, headphones, shoes..." autocomplete="off" id="headerSearchInput">
        <div class="search-dropdown" id="searchDropdown"></div>
      </form>

      <!-- Nav Actions -->
      <div class="nav-actions">
        <button class="action-btn" id="themeToggleBtn" title="Toggle Theme">
          <span id="themeIcon">🌙</span>
        </button>

        {% if user.is_authenticated %}
        <a href="{% url 'wishlist' %}" class="action-btn" title="Wishlist">
          <span>❤️</span>
          <span class="badge-count" id="wishlistBadge">{{ wishlist_count }}</span>
        </a>
        {% else %}
        <a href="{% url 'login' %}?next={% url 'wishlist' %}" class="action-btn" title="Wishlist">
          <span>❤️</span>
        </a>
        {% endif %}

        <a href="{% url 'cart' %}" class="action-btn" id="navCartBtn" title="Shopping Cart">
          <span>🛒</span>
          <span class="badge-count" id="cartBadge">{{ cart_count }}</span>
        </a>

        {% if user.is_authenticated %}
        <a href="{% url 'profile' %}" class="btn btn-secondary btn-sm" style="margin-left:0.25rem;">
          👤 {{ user.first_name|default:user.username }}
        </a>
        <a href="{% url 'logout' %}" class="btn btn-secondary btn-sm" title="Logout">Exit</a>
        {% else %}
        <a href="{% url 'login' %}" class="btn btn-secondary btn-sm">Login</a>
        <a href="{% url 'register' %}" class="btn btn-primary btn-sm">Register</a>
        {% endif %}
      </div>
    </div>
  </header>

  <!-- Messages / Alerts -->
  <div class="toast-container">
    {% if messages %}
      {% for message in messages %}
        <div class="toast toast-{{ message.tags|default:'success' }}">
          <span>{{ message }}</span>
        </div>
      {% endfor %}
    {% endif %}
  </div>

  <!-- Main Content -->
  <main style="flex:1;">
    {% block content %}{% endblock %}
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a href="{% url 'home' %}" class="brand-logo" style="margin-bottom:0.75rem;">NEXORA</a>
          <p class="footer-desc">Smart Shopping, Simplified. A modern, AI-powered e-commerce ecosystem built for seamless discovery and elevated living.</p>
          <div style="display:flex;gap:1rem;color:var(--text-dim);font-size:1.2rem;">
            <span>🌐</span> <span>🐦</span> <span>📸</span> <span>💼</span>
          </div>
        </div>

        <div>
          <h4 class="footer-title">Shop</h4>
          <ul class="footer-links">
            <li><a href="{% url 'product_list' %}" class="footer-link">All Products</a></li>
            {% for cat in global_categories %}
            <li><a href="{% url 'product_list' %}?category={{ cat.slug }}" class="footer-link">{{ cat.name }}</a></li>
            {% endfor %}
            <li><a href="{% url 'home' %}#flash-deals" class="footer-link">Flash Deals</a></li>
          </ul>
        </div>

        <div>
          <h4 class="footer-title">Account</h4>
          <ul class="footer-links">
            {% if user.is_authenticated %}
            <li><a href="{% url 'profile' %}" class="footer-link">My Profile</a></li>
            <li><a href="{% url 'wishlist' %}" class="footer-link">Wishlist</a></li>
            <li><a href="{% url 'cart' %}" class="footer-link">Shopping Cart</a></li>
            <li><a href="{% url 'order_tracking' %}" class="footer-link">Track Orders</a></li>
            <li><a href="{% url 'logout' %}" class="footer-link">Sign Out</a></li>
            {% else %}
            <li><a href="{% url 'login' %}" class="footer-link">Sign In</a></li>
            <li><a href="{% url 'register' %}" class="footer-link">Create Account</a></li>
            <li><a href="{% url 'order_tracking' %}" class="footer-link">Track Order</a></li>
            {% endif %}
          </ul>
        </div>

        <div>
          <h4 class="footer-title">Customer Care</h4>
          <ul class="footer-links">
            <li><a href="{% url 'order_tracking' %}" class="footer-link">Order Status</a></li>
            <li><a href="{% url 'home' %}#ai-assistant" class="footer-link">AI Shopping Assistant</a></li>
            <li><a href="{% url 'compare' %}" class="footer-link">Product Comparison</a></li>
            <li><a href="#" class="footer-link">Shipping & Returns</a></li>
            <li><a href="/admin/" class="footer-link" style="color:var(--accent);">Django Admin</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <div>&copy; 2026 NEXORA Inc. All rights reserved. Built with Django & Modern Web Standards.</div>
        <div style="display:flex;gap:1.5rem;">
          <a href="#" class="footer-link">Privacy Policy</a>
          <a href="#" class="footer-link">Terms of Service</a>
          <a href="#" class="footer-link">Security</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Scripts -->
  <script src="{% static 'js/theme.js' %}"></script>
  <script src="{% static 'js/cart.js' %}"></script>
  <script>
    // Header search autocomplete
    const searchInput = document.getElementById('headerSearchInput');
    const searchDrop = document.getElementById('searchDropdown');
    if (searchInput && searchDrop) {
      let timer = null;
      searchInput.addEventListener('input', () => {
        clearTimeout(timer);
        const q = searchInput.value.trim();
        if (q.length < 2) {
          searchDrop.style.display = 'none';
          return;
        }
        timer = setTimeout(() => {
          fetch('/api/search-suggest/?q=' + encodeURIComponent(q))
            .then(res => res.json())
            .then(data => {
              if (data.results && data.results.length > 0) {
                let html = '';
                data.results.forEach(item => {
                  html += '<a href="/product/' + item.slug + '/" class="search-result-item">' +
                    '<img src="' + item.image + '" class="search-result-thumb">' +
                    '<div><div style="font-weight:600;font-size:0.9rem;">' + item.name + '</div>' +
                    '<div style="font-size:0.8rem;color:var(--primary);font-weight:700;">₹' + item.current_price.toLocaleString('en-IN') + '</div></div></a>';
                });
                searchDrop.innerHTML = html;
                searchDrop.style.display = 'block';
              } else {
                searchDrop.style.display = 'none';
              }
            });
        }, 250);
      });
      document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchDrop.contains(e.target)) {
          searchDrop.style.display = 'none';
        }
      });
    }
  </script>
  {% block extra_js %}{% endblock %}
</body>
</html>
"""
with open("store/templates/store/base.html", "w", encoding="utf-8") as f:
    f.write(base_html)
print("[OK] base.html written")

# 2. home.html
home_html = """{% extends 'store/base.html' %}
{% load static %}

{% block title %}NEXORA | Smart Shopping, Simplified{% endblock %}

{% block content %}
<!-- 1. Hero Section -->
<section class="hero-section">
  <div class="container hero-grid">
    <div>
      <div class="hero-badge">✨ Next-Generation Intelligent E-Commerce</div>
      <h1 class="hero-title">
        NEXORA<br>
        <span class="gradient-text">Smart Shopping, Simplified.</span>
      </h1>
      <p class="hero-desc">Discover products that fit your style, needs and budget. Driven by precision craftsmanship, responsive performance, and AI-powered recommendations.</p>
      
      <div class="hero-buttons">
        <a href="{% url 'product_list' %}" class="btn btn-primary">
          Explore Products <span>→</span>
        </a>
        <a href="{% url 'product_list' %}?sort=popular" class="btn btn-secondary">
          🔥 Shop Trending
        </a>
      </div>
    </div>

    <div class="hero-visual">
      <div class="hero-img-card">
        <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=900&q=80" alt="Hero Featured Product" class="hero-img">
      </div>

      <div class="floating-pill pill-1">
        <span style="font-size:1.4rem;">🎧</span>
        <div>
          <div style="font-size:0.75rem;color:var(--text-muted);">Trending Tech</div>
          <div style="font-weight:700;font-size:0.9rem;">AeroSound Pro ANC</div>
        </div>
      </div>

      <div class="floating-pill pill-2">
        <span style="font-size:1.4rem;">⚡</span>
        <div>
          <div style="font-size:0.75rem;color:var(--text-muted);">Flash Deal</div>
          <div style="font-weight:700;font-size:0.9rem;color:var(--accent);">Save 44% Today</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- 2. Categories Section -->
<section class="section" id="categories">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Collections</div>
      <h2 class="section-title">Shop by Category</h2>
      <p class="section-subtitle">Curated categories meticulously designed for modern lifestyles.</p>
    </div>

    <div class="category-grid">
      {% for cat in categories %}
      <a href="{% url 'product_list' %}?category={{ cat.slug }}" class="category-card">
        <img src="{{ cat.image_url }}" alt="{{ cat.name }}" class="category-bg">
        <div class="category-info">
          <div class="category-name">
            {{ cat.name }}
            <span class="category-arrow">→</span>
          </div>
          <div style="font-size:0.8rem;color:rgba(255,255,255,0.8);">{{ cat.product_count }} Products</div>
        </div>
      </a>
      {% endfor %}
    </div>
  </div>
</section>

<!-- 3. Interactive Product Showcase ("Discover Your Next Favorite") -->
{% if showcase_product %}
<section class="section">
  <div class="container">
    <div class="showcase-box">
      <div>
        <div class="section-tag">Featured Spotlight</div>
        <h2 class="section-title" style="font-size:2.6rem;margin-bottom:1rem;">Discover Your Next Favorite.</h2>
        <p style="font-size:1.15rem;color:var(--text-muted);margin-bottom:1.5rem;">{{ showcase_product.description|truncatewords:28 }}</p>
        
        <div style="display:flex;align-items:baseline;gap:1rem;margin-bottom:2rem;">
          <span class="current-price" style="font-size:2.2rem;color:var(--text-main);">₹{{ showcase_product.current_price }}</span>
          {% if showcase_product.has_discount %}
          <span class="original-price" style="font-size:1.25rem;">₹{{ showcase_product.price }}</span>
          <span class="discount-badge" style="position:static;">Save {{ showcase_product.discount_percentage }}%</span>
          {% endif %}
        </div>

        <div style="display:flex;gap:1rem;">
          <button onclick="addToCart({{ showcase_product.id }}, 1, this)" class="btn btn-primary">
            Add to Cart 🛒
          </button>
          <a href="{% url 'product_detail' showcase_product.slug %}" class="btn btn-secondary">
            View Details ↗
          </a>
        </div>
      </div>

      <div class="showcase-visual">
        <img src="{{ showcase_product.main_image }}" alt="{{ showcase_product.name }}">
      </div>
    </div>
  </div>
</section>
{% endif %}

<!-- 4. Trending Now -->
<section class="section" style="background:var(--bg-surface);">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">Popular Picks</div>
      <h2 class="section-title">🔥 Trending Now</h2>
      <p class="section-subtitle">Top rated products customers are loving this week.</p>
    </div>

    <div class="product-grid">
      {% for product in trending_products %}
      <div class="product-card">
        <div class="product-thumb-wrap">
          <a href="{% url 'product_detail' product.slug %}">
            <img src="{{ product.main_image }}" alt="{{ product.name }}" class="product-thumb">
          </a>
          {% if product.has_discount %}
          <span class="discount-badge">-{{ product.discount_percentage }}%</span>
          {% endif %}
          <button class="wishlist-btn {% if product.id in user_wishlist_ids %}active{% endif %}" onclick="toggleWishlist({{ product.id }}, this)" title="Wishlist">
            ❤️
          </button>
        </div>

        <div class="product-content">
          <div class="product-category-tag">{{ product.category.name }}</div>
          <h3 class="product-name">
            <a href="{% url 'product_detail' product.slug %}">{{ product.name }}</a>
          </h3>
          <div class="product-rating">
            ★ {{ product.rating }} <span class="product-reviews-count">({{ product.reviews_count }})</span>
          </div>
          <div class="product-price-row">
            <span class="current-price">₹{{ product.current_price }}</span>
            {% if product.has_discount %}
            <span class="original-price">₹{{ product.price }}</span>
            {% endif %}
          </div>
          <div class="product-card-actions">
            <a href="{% url 'product_detail' product.slug %}" class="btn btn-secondary btn-sm">Details</a>
            <button onclick="addToCart({{ product.id }}, 1, this)" class="btn btn-primary btn-sm">Add to Cart</button>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<!-- 5. Flash Deals with Live Countdown -->
<section class="section" id="flash-deals">
  <div class="container">
    <div class="flash-deals-banner">
      <div>
        <div style="text-transform:uppercase;font-size:0.8rem;letter-spacing:1.5px;color:var(--accent);font-weight:700;margin-bottom:0.25rem;">Limited Time Offers</div>
        <h2 style="font-size:2rem;font-weight:800;">⚡ Flash Deals</h2>
        <p style="color:var(--text-muted);font-size:0.95rem;">Unbeatable discounts on high-demand premium products. Don't miss out.</p>
      </div>

      <div class="countdown-timer" id="flashCountdown">
        <div class="countdown-unit">
          <div class="countdown-val" id="dealHours">02</div>
          <div class="countdown-label">Hours</div>
        </div>
        <div class="countdown-sep">:</div>
        <div class="countdown-unit">
          <div class="countdown-val" id="dealMins">14</div>
          <div class="countdown-label">Mins</div>
        </div>
        <div class="countdown-sep">:</div>
        <div class="countdown-unit">
          <div class="countdown-val" id="dealSecs">35</div>
          <div class="countdown-label">Secs</div>
        </div>
      </div>
    </div>

    <div class="product-grid">
      {% for product in flash_deals %}
      <div class="product-card">
        <div class="product-thumb-wrap">
          <a href="{% url 'product_detail' product.slug %}">
            <img src="{{ product.main_image }}" alt="{{ product.name }}" class="product-thumb">
          </a>
          <span class="discount-badge" style="background:var(--accent);">⚡ SAVE {{ product.discount_percentage }}%</span>
          <button class="wishlist-btn {% if product.id in user_wishlist_ids %}active{% endif %}" onclick="toggleWishlist({{ product.id }}, this)">
            ❤️
          </button>
        </div>

        <div class="product-content">
          <div class="product-category-tag">{{ product.category.name }}</div>
          <h3 class="product-name"><a href="{% url 'product_detail' product.slug %}">{{ product.name }}</a></h3>
          <div class="product-rating">★ {{ product.rating }} ({{ product.reviews_count }})</div>
          <div class="product-price-row">
            <span class="current-price" style="color:var(--accent);">₹{{ product.current_price }}</span>
            <span class="original-price">₹{{ product.price }}</span>
          </div>
          <div class="product-card-actions">
            <a href="{% url 'product_detail' product.slug %}" class="btn btn-secondary btn-sm">Details</a>
            <button onclick="addToCart({{ product.id }}, 1, this)" class="btn btn-primary btn-sm">Add to Cart</button>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<!-- 6. AI Shopping Assistant ("Not Sure What to Buy?") -->
<section class="section" id="ai-assistant">
  <div class="container">
    <div class="ai-assistant-wrapper">
      <div class="ai-header-badge">🤖 AI Shopping Assistant</div>
      <h2 style="font-size:2.2rem;font-weight:800;margin-bottom:0.5rem;">Not Sure What to Buy?</h2>
      <p style="color:var(--text-muted);font-size:1.1rem;max-width:600px;">Tell NEXORA what you need in plain English, and our smart recommendation engine will find the best match for your style, specs, and budget.</p>

      <div class="ai-chips-wrap">
        <span class="ai-chip" data-prompt="I need wireless headphones under ₹5000 for gaming">🎧 Wireless headphones under ₹5000</span>
        <span class="ai-chip" data-prompt="Show me running shoes with good cushioning under ₹10000">👟 Running shoes under ₹10000</span>
        <span class="ai-chip" data-prompt="Looking for a mechanical keyboard for coding">⌨️ Mechanical keyboard for coding</span>
        <span class="ai-chip" data-prompt="Minimalist leather jacket under ₹12000">🧥 Leather jacket under ₹12000</span>
        <span class="ai-chip" data-prompt="Ergonomic desk chair for home office">🪑 Ergonomic desk chair</span>
      </div>

      <div class="ai-input-group">
        <input type="text" id="aiPromptInput" class="ai-input" placeholder="e.g. 'I need wireless headphones under ₹5000 for gaming'...">
        <button id="aiSendBtn" class="btn btn-primary" style="padding:0.9rem 2rem;">Ask AI 🚀</button>
      </div>

      <!-- AI Dynamic Results -->
      <div class="ai-results-area" id="aiResultsArea">
        <div class="ai-reply-bubble" id="aiReplyBubble"></div>
        <div class="product-grid" id="aiProductsGrid"></div>
      </div>
    </div>
  </div>
</section>

<!-- 7. Recently Viewed -->
{% if recently_viewed %}
<section class="section" style="padding-top:2rem;">
  <div class="container">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:2rem;">
      <h2 style="font-size:1.75rem;font-weight:800;">Recently Viewed</h2>
      <a href="{% url 'product_list' %}" style="color:var(--primary);font-weight:600;">View All →</a>
    </div>

    <div class="product-grid" style="grid-template-columns:repeat(auto-fill, minmax(220px, 1fr));">
      {% for product in recently_viewed %}
      <div class="product-card">
        <div class="product-thumb-wrap" style="height:190px;">
          <a href="{% url 'product_detail' product.slug %}">
            <img src="{{ product.main_image }}" alt="{{ product.name }}" class="product-thumb">
          </a>
        </div>
        <div class="product-content" style="padding:1rem;">
          <h4 style="font-size:0.95rem;font-weight:700;margin-bottom:0.35rem;"><a href="{% url 'product_detail' product.slug %}">{{ product.name|truncatechars:28 }}</a></h4>
          <div class="current-price" style="font-size:1.1rem;margin-bottom:0.75rem;">₹{{ product.current_price }}</div>
          <button onclick="addToCart({{ product.id }}, 1, this)" class="btn btn-secondary btn-sm btn-block">Add to Cart</button>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>
{% endif %}
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/deals.js' %}"></script>
<script src="{% static 'js/assistant.js' %}"></script>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    initFlashDeals("{{ deal_deadline }}");
  });
</script>
{% endblock %}
"""
with open("store/templates/store/home.html", "w", encoding="utf-8") as f:
    f.write(home_html)
print("[OK] home.html written")

print("Templates step 1 complete.")
