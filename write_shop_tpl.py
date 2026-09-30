import os

tpl1 = """{% extends 'store/base.html' %}
{% load static %}
{% block title %}Shop All Products | NEXORA{% endblock %}
{% block content %}
<div class="container" style="padding:3rem 1.5rem;">
  <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:2rem;flex-wrap:wrap;gap:1rem;">
    <div>
      <h1 style="font-size:2.4rem;font-weight:800;letter-spacing:-0.5px;">Explore Products</h1>
      <p style="color:var(--text-muted);">Showing {{ total_count }} items</p>
    </div>
    <form method="GET" id="sortForm" style="display:flex;align-items:center;gap:0.75rem;">
      {% if selected_category %}<input type="hidden" name="category" value="{{ selected_category }}">{% endif %}
      {% if query %}<input type="hidden" name="q" value="{{ query }}">{% endif %}
      <label style="font-size:0.9rem;color:var(--text-muted);font-weight:600;">Sort By:</label>
      <select name="sort" onchange="document.getElementById('sortForm').submit();" class="form-control" style="width:auto;padding:0.4rem 0.8rem;">
        <option value="popular" {% if sort_by == 'popular' %}selected{% endif %}>Most Popular</option>
        <option value="rating" {% if sort_by == 'rating' %}selected{% endif %}>Highest Rated</option>
        <option value="price_low" {% if sort_by == 'price_low' %}selected{% endif %}>Price: Low to High</option>
        <option value="price_high" {% if sort_by == 'price_high' %}selected{% endif %}>Price: High to Low</option>
        <option value="newest" {% if sort_by == 'newest' %}selected{% endif %}>Newest First</option>
      </select>
    </form>
  </div>

  <div style="display:grid;grid-template-columns:250px 1fr;gap:2rem;align-items:start;">
    <aside style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-md);padding:1.5rem;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;">
        <h3 style="font-size:1.1rem;font-weight:700;">Filters</h3>
        <a href="{% url 'product_list' %}" style="font-size:0.8rem;color:var(--primary);font-weight:600;">Reset</a>
      </div>
      <form method="GET">
        {% if query %}<input type="hidden" name="q" value="{{ query }}">{% endif %}
        <div style="margin-bottom:1.5rem;">
          <h4 style="font-size:0.85rem;text-transform:uppercase;color:var(--text-dim);margin-bottom:0.75rem;">Categories</h4>
          <div style="display:flex;flex-direction:column;gap:0.5rem;font-size:0.9rem;">
            <a href="{% url 'product_list' %}" style="color:{% if not selected_category %}var(--primary);font-weight:700{% else %}var(--text-muted){% endif %};">All Products</a>
            {% for cat in categories %}
            <a href="{% url 'product_list' %}?category={{ cat.slug }}" style="display:flex;justify-content:space-between;color:{% if selected_category == cat.slug %}var(--primary);font-weight:700{% else %}var(--text-muted){% endif %};">
              <span>{{ cat.name }}</span>
              <span style="color:var(--text-dim);font-size:0.8rem;">({{ cat.product_count }})</span>
            </a>
            {% endfor %}
          </div>
        </div>

        <div style="margin-bottom:1.5rem;">
          <h4 style="font-size:0.85rem;text-transform:uppercase;color:var(--text-dim);margin-bottom:0.75rem;">Price (₹)</h4>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;">
            <input type="number" name="min_price" value="{{ min_price }}" placeholder="Min" class="form-control" style="padding:0.4rem;font-size:0.85rem;">
            <input type="number" name="max_price" value="{{ max_price }}" placeholder="Max" class="form-control" style="padding:0.4rem;font-size:0.85rem;">
          </div>
        </div>

        <div style="margin-bottom:1.5rem;">
          <label style="display:flex;align-items:center;gap:0.5rem;font-size:0.9rem;cursor:pointer;">
            <input type="checkbox" name="in_stock" value="1" {% if in_stock_only == '1' %}checked{% endif %}>
            <span>In Stock Only</span>
          </label>
        </div>

        <button type="submit" class="btn btn-primary btn-block btn-sm">Filter</button>
      </form>
    </aside>

    <div>
      {% if products %}
      <div class="product-grid">
        {% for product in products %}
        <div class="product-card">
          <div class="product-thumb-wrap">
            <a href="{% url 'product_detail' product.slug %}">
              <img src="{{ product.main_image }}" alt="{{ product.name }}" class="product-thumb">
            </a>
            {% if product.has_discount %}<span class="discount-badge">-{{ product.discount_percentage }}%</span>{% endif %}
            <button class="wishlist-btn {% if product.id in user_wishlist_ids %}active{% endif %}" onclick="toggleWishlist({{ product.id }}, this)">❤️</button>
          </div>
          <div class="product-content">
            <div class="product-category-tag">{{ product.category.name }}</div>
            <h3 class="product-name"><a href="{% url 'product_detail' product.slug %}">{{ product.name }}</a></h3>
            <div class="product-rating">★ {{ product.rating }} ({{ product.reviews_count }})</div>
            <div class="product-price-row">
              <span class="current-price">₹{{ product.current_price }}</span>
              {% if product.has_discount %}<span class="original-price">₹{{ product.price }}</span>{% endif %}
            </div>
            <div class="product-card-actions">
              <a href="{% url 'product_detail' product.slug %}" class="btn btn-secondary btn-sm">Details</a>
              <button onclick="addToCart({{ product.id }}, 1, this)" class="btn btn-primary btn-sm">Add to Cart</button>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
      {% else %}
      <div style="text-align:center;padding:4rem 2rem;background:var(--bg-card);border-radius:var(--radius-md);">
        <h3>No products found</h3>
        <p style="color:var(--text-muted);margin:1rem 0;">Try adjusting your search or filters.</p>
        <a href="{% url 'product_list' %}" class="btn btn-primary btn-sm">Clear Filters</a>
      </div>
      {% endif %}
    </div>
  </div>
</div>
{% endblock %}
"""

with open("store/templates/store/product_list.html", "w", encoding="utf-8") as f:
    f.write(tpl1)
print("[OK] product_list.html written")
