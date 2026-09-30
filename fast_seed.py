import os
import sys
import django
import json
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nexora_project.settings")
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, Order, OrderItem, UserAddress

# Superuser
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@nexora.com", "admin123")
    print("[OK] Admin created: admin / admin123")

# Demo user
user, created = User.objects.get_or_create(
    username="john_doe",
    defaults={"email": "john.doe@example.com", "first_name": "John", "last_name": "Doe"}
)
if created:
    user.set_password("password123")
    user.save()
    print("[OK] Demo user created: john_doe / password123")

# Categories
cats = [
    ("Electronics", "electronics", "Next-gen personal tech, audio & displays.", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80"),
    ("Fashion", "fashion", "Elevated essentials, streetwear and luxury.", "https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&q=80"),
    ("Beauty", "beauty", "Clean formulations, active botanicals & radiance.", "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&q=80"),
    ("Home & Living", "home-living", "Minimalist ergonomics & ambient living.", "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80"),
    ("Accessories", "accessories", "Precision titanium timepieces & leather.", "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80"),
    ("Sports", "sports", "High-performance gear & home strength.", "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&q=80"),
]

cat_map = {}
for name, slug, desc, img in cats:
    c, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc, "image_url": img})
    cat_map[slug] = c

# Products
products = [
    ("electronics", "AeroSound Pro Wireless Headphones", "aerosound-pro-wireless-headphones", "Studio-grade ANC headphones with 45 hours battery life.", 8999, 4999, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80", 4.9, 142, True, True, True),
    ("electronics", "ZenithFlow Mechanical Keyboard", "zenithflow-mechanical-keyboard", "CNC aluminum low-profile mechanical keyboard with hot-swappable switches.", 9499, 7299, "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80", 4.8, 89, True, True, False),
    ("electronics", "Vanguard UltraVision 32 4K Monitor", "vanguard-ultravision-32-4k-monitor", "IPS Black 4K HDR display with 90W Type-C Thunderbolt power.", 48999, 42999, "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80", 4.9, 56, True, False, False),
    ("electronics", "NovaPulse True Wireless Earbuds", "novapulse-true-wireless-earbuds", "IPX7 waterproof earbuds with AI environmental noise reduction.", 4999, 2799, "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80", 4.7, 210, False, True, True),
    ("fashion", "Heritage Nappa Biker Leather Jacket", "heritage-nappa-biker-leather-jacket", "Handcrafted Italian full-grain lambskin with gunmetal hardware.", 14999, 9999, "https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?w=800&q=80", 4.9, 64, True, True, False),
    ("fashion", "Minimalist French Terry Hoodie", "minimalist-french-terry-hoodie", "500 GSM heavyweight organic cotton boxy relaxed silhouette.", 4499, 2999, "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&q=80", 4.8, 118, False, True, True),
    ("fashion", "Apex All-Day Stretch Chinos", "apex-all-day-stretch-chinos", "Water-repellent 4-way stretch tailored trousers.", 3499, 2299, "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80", 4.6, 74, False, False, False),
    ("beauty", "LumiCell Multi-Peptide Glow Serum", "lumicell-multi-peptide-glow-serum", "Multi-peptide complex with 5% Niacinamide and Hyaluronic Acid.", 2499, 1699, "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=80", 4.9, 188, True, True, True),
    ("beauty", "Botanical Radiance Restorative Face Oil", "botanical-radiance-restorative-face-oil", "Cold-pressed rosehip and marula with Vitamin C and CoQ10.", 2999, 2199, "https://images.unsplash.com/photo-1608248597359-bb436329a4a7?w=800&q=80", 4.8, 92, False, False, False),
    ("home-living", "AuraCloud Ultrasonic Aroma Diffuser", "auracloud-ultrasonic-aroma-diffuser", "Handmade ceramic diffuser with warm ambient halo LED nightlight.", 3999, 2499, "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&q=80", 4.9, 156, True, True, False),
    ("home-living", "ErgoPosture Zero-Gravity Executive Chair", "ergoposture-zero-gravity-executive-chair", "Breathable German elastomeric tension mesh with dynamic 3D lumbar support.", 24999, 18999, "https://images.unsplash.com/photo-1580481077195-c3a821a58875?w=800&q=80", 4.8, 77, True, False, False),
    ("accessories", "Chronos Titanium Minimalist Smartwatch", "chronos-titanium-minimalist-smartwatch", "Grade-5 titanium case, AMOLED sapphire screen with 14-day battery.", 18999, 14999, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80", 4.9, 124, True, True, False),
    ("accessories", "Solaris Aviator Polarized Sunglasses", "solaris-aviator-polarized-sunglasses", "Surgical stainless steel wireframe with UV400 polarized lenses.", 3299, 1999, "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=80", 4.7, 82, False, True, False),
    ("sports", "Velocity Carbon-Plate Pro Running Shoes", "velocity-carbon-plate-pro-running-shoes", "Full-length curved carbon fiber propulsion plate with Pebax foam.", 11999, 7999, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80", 4.9, 195, True, True, False),
    ("sports", "IronFlex Smart Quick-Adjust Dumbbells", "ironflex-smart-quick-adjust-dumbbells", "Replaces 15 pairs. Adjustable from 2.5kg to 24kg with single dial.", 16999, 12999, "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&q=80", 4.8, 110, True, False, False)
]

for c_slug, name, slug, desc, price, d_price, img, rating, reviews, feat, trend, flash in products:
    Product.objects.update_or_create(
        slug=slug,
        defaults={
            "category": cat_map[c_slug],
            "name": name,
            "description": desc,
            "price": Decimal(str(price)),
            "discount_price": Decimal(str(d_price)),
            "main_image": img,
            "rating": rating,
            "reviews_count": reviews,
            "is_featured": feat,
            "is_trending": trend,
            "is_flash_deal": flash,
            "stock": 25
        }
    )

print("[OK] Products seeded successfully:", Product.objects.count())
