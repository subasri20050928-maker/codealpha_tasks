import os
import django
import json
from decimal import Decimal
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexora_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import (
    Category, Product, ProductImage, Review,
    Order, OrderItem, UserAddress
)

def run_seed():
    print(🌱 Seeding NEXORA database...)

    # 1. Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@nexora.com', 'admin123')
        print(✓ Created superuser: admin / admin123)
    else:
        print(✓ Superuser admin already exists)

    # 2. Create Demo User
    demo_user, created = User.objects.get_or_create(
        username='john_doe',
        defaults={
            'email': 'john.doe@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }
    )
    if created:
        demo_user.set_password('password123')
        demo_user.save()
        print(✓ Created demo user: john_doe / password123)
    else:
        print(✓ Demo user john_doe already exists)

    # Demo user address
    UserAddress.objects.get_or_create(
        user=demo_user,
        defaults={
            'full_name': 'John Doe',
            'phone': '+91 98765 43210',
            'address_line': 'Flat 402, Skyline Heights, Cyber City',
            'city': 'Bengaluru',
            'state': 'Karnataka',
            'pincode': '560100',
            'is_default': True
        }
    )

    # 3. Categories
    categories_data = [
        {
            'name': 'Electronics',
            'slug': 'electronics',
            'description': 'Next-gen audio, computing, and cutting-edge personal tech.',
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
            'icon': 'bi-laptop'
        },
        {
            'name': 'Fashion',
            'slug': 'fashion',
            'description': 'Elevated essentials, modern streetwear, and timeless luxury.',
            'image_url': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&q=80',
            'icon': 'bi-bag'
        },
        {
            'name': 'Beauty',
            'slug': 'beauty',
            'description': 'Clean formulations, active botanicals, and daily radiance.',
            'image_url': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=800&q=80',
            'icon': 'bi-stars'
        },
        {
            'name': 'Home & Living',
            'slug': 'home-living',
            'description': 'Minimalist ergonomics, artisanal ceramics, and ambient comfort.',
            'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80',
            'icon': 'bi-house'
        },
        {
            'name': 'Accessories',
            'slug': 'accessories',
            'description': 'Precision titanium timepieces, leathercraft, and optical wear.',
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
            'icon': 'bi-watch'
        },
        {
            'name': 'Sports',
            'slug': 'sports',
            'description': 'High-performance athletic gear, footwear, and home gym strength.',
            'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=800&q=80',
            'icon': 'bi-activity'
        },
    ]

    cat_objs = {}
    for cdata in categories_data:
        cat, _ = Category.objects.update_or_create(
            slug=cdata['slug'],
            defaults=cdata
        )
        cat_objs[cdata['slug']] = cat
    print(f✓ Seeded {len(cat_objs)} categories)

    # 4. Products
    products_data = [
        # Electronics
        {
            'category': cat_objs['electronics'],
            'name': 'AeroSound Pro Wireless Headphones',
            'slug': 'aerosound-pro-wireless-headphones',
            'description': 'Engineered with custom 40mm beryllium drivers and hybrid active noise cancellation. Delivers studio-grade high resolution acoustics with ultra-low latency and up to 45 hours of continuous playback on a single charge.',
            'specifications': json.dumps({
                'Driver Size': '40mm Custom Beryllium',
                'ANC': 'Hybrid Adaptive ANC (Up to 42dB reduction)',
                'Battery Life': '45 Hours (ANC off), 35 Hours (ANC on)',
                'Connectivity': 'Bluetooth 5.3 + 3.5mm Lossless Audio',
                'Weight': '248g',
                'Fast Charging': '10 mins charge = 5 hours playback'
            }),
            'price': Decimal('8999.00'),
            'discount_price': Decimal('4999.00'),
            'main_image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80',
            'stock': 24,
            'rating': 4.9,
            'reviews_count': 142,
            'is_featured': True,
            'is_trending': True,
            'is_flash_deal': True,
        },
        {
            'category': cat_objs['electronics'],
            'name': 'ZenithFlow Ultra-Slim Mechanical Keyboard',
            'slug': 'zenithflow-ultra-slim-mechanical-keyboard',
            'description': 'A CNC anodized aluminum 75% low-profile mechanical keyboard featuring hot-swappable tactile switches, RGB per-key backlighting, and seamless triple-mode Bluetooth, 2.4GHz wireless and Type-C wired connectivity.',
            'specifications': json.dumps({
                'Switch Type': 'Gateron Low-Profile Tactile Banana',
                'Connectivity': 'Tri-Mode (Bluetooth 5.2 / 2.4GHz / USB-C)',
                'Chassis': 'CNC Machined Anodized Aerospace Aluminum',
                'Keycaps': 'Double-shot PBT Low Profile',
                'Battery': '4000mAh Rechargeable Li-ion'
            }),
            'price': Decimal('9499.00'),
            'discount_price': Decimal('7299.00'),
            'main_image': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80',
            'stock': 18,
            'rating': 4.8,
            'reviews_count': 89,
            'is_featured': True,
            'is_trending': True,
            'is_flash_deal': False,
        },
        {
            'category': cat_objs['electronics'],
            'name': 'Vanguard UltraVision 32 4K HDR Monitor',
 'slug': 'vanguard-ultravision-32-4k-hdr-monitor',
 'description': 'Tailored for creators, developers, and power users. Featuring 99% DCI-P3 color gamut, factory calibration (Delta E < 1.5), 90W USB-C single cable power delivery, and an ergonomic zero-gravity stand.',
 'specifications': json.dumps({
 'Panel Type': 'IPS Black 32-inch 4K UHD (3840 x 2160)',
 'Color Accuracy': '99% DCI-P3, 100% sRGB, Delta E < 1.5',
 'Refresh Rate': '120Hz Adaptive-Sync',
 'Ports': 'Thunderbolt 4 (90W PD), HDMI 2.1, DP 1.4, USB Hub',
 'Stand': 'Height, Pivot, Tilt, Swivel Ergonomic Arm'
 }),
 'price': Decimal('48999.00'),
 'discount_price': Decimal('42999.00'),
 'main_image': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=800&q=80',
 'stock': 12,
 'rating': 4.9,
 'reviews_count': 56,
 'is_featured': True,
 'is_trending': False,
 'is_flash_deal': False,
 },
 {
 'category': cat_objs['electronics'],
 'name': 'NovaPulse True Wireless Earbuds',
 'slug': 'novapulse-true-wireless-earbuds',
 'description': 'Ultra-compact IPX7 water-resistant earbuds engineered with dual dynamic armature drivers, environmental beamforming mics, and wireless Qi quick-charging case.',
 'specifications': json.dumps({
 'Water Resistance': 'IPX7 Sweat & Water Resistant',
 'Driver': '10mm Bio-Cellulose Dynamic Drivers',
 'Playback Time': '32 Hours with Case',
 'Microphone': 'Quad-Mic array with cVc 8.0 AI Call Noise Reduction'
 }),
 'price': Decimal('4999.00'),
 'discount_price': Decimal('2799.00'),
 'main_image': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&q=80',
 'stock': 35,
 'rating': 4.7,
 'reviews_count': 210,
 'is_featured': False,
 'is_trending': True,
 'is_flash_deal': True,
 },

 # Fashion
 {
 'category': cat_objs['fashion'],
 'name': 'Heritage Nappa Biker Leather Jacket',
 'slug': 'heritage-nappa-biker-leather-jacket',
 'description': 'Handcrafted from 100% supple full-grain Italian nappa lambskin leather. Features matte gunmetal YKK hardware, tailored asymmetrical cut, and breathable satin interior lining.',
 'specifications': json.dumps({
 'Material': '100% Full-Grain Italian Nappa Lambskin',
 'Hardware': 'Heavy-Duty Gunmetal YKK Zippers',
 'Lining': 'Smooth Breathable Cupro Satin',
 'Fit': 'Contemporary Tailored Slim Fit',
 'Care': 'Professional Leather Clean Only'
 }),
 'price': Decimal('14999.00'),
 'discount_price': Decimal('9999.00'),
 'main_image': 'https://images.unsplash.com/photo-1521223890158-f9f7c3d5d504?w=800&q=80',
 'stock': 14,
 'rating': 4.9,
 'reviews_count': 64,
 'is_featured': True,
 'is_trending': True,
 'is_flash_deal': False,
 },
 {
 'category': cat_objs['fashion'],
 'name': 'Minimalist Heavyweight French Terry Hoodie',
 'slug': 'minimalist-heavyweight-french-terry-hoodie',
 'description': '500 GSM organic looped French terry cotton woven for supreme structure and warmth. Features a clean double-layered hood without drawstrings, dropped shoulders, and ribbed cuffs.',
 'specifications': json.dumps({
 'Fabric': '500 GSM 100% Organic Combed Cotton',
 'Weave': 'Heavyweight Looped French Terry',
 'Fit': 'Modern Relaxed Boxy Silhouette',
 'Origin': 'Ethically Milled & Dyed'
 }),
 'price': Decimal('4499.00'),
 'discount_price': Decimal('2999.00'),
 'main_image': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=800&q=80',
 'stock': 40,
 'rating': 4.8,
 'reviews_count': 118,
 'is_featured': False,
 'is_trending': True,
 'is_flash_deal': True,
 },
 {
 'category': cat_objs['fashion'],
 'name': 'Apex All-Day Stretch Chino Trousers',
 'slug': 'apex-all-day-stretch-chino-trousers',
 'description': 'Constructed from premium 4-way stretch cotton twill with water-repellent nanocoating. Designed for all-day comfort whether traveling, working at the desk, or evening dinners.',
 'specifications': json.dumps({
 'Composition': '96% Long-Staple Cotton, 4% Elastane',
 'Finish': 'Stain & Water Repellent Eco-Shield',
 'Waistband': 'Hidden Stretch Comfort Flex Band',
 'Pockets': 'Deep Front Slash + Hidden Zipper Security Pocket'
 }),
 'price': Decimal('3499.00'),
 'discount_price': Decimal('2299.00'),
 'main_image': 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80',
 'stock': 25,
 'rating': 4.6,
 'reviews_count': 74,
 'is_featured': False,
 'is_trending': False,
 'is_flash_deal': False,
 },

 # Beauty
 {
 'category': cat_objs['beauty'],
 'name': 'LumiCell Multi-Peptide Glow Serum',
 'slug': 'lumicell-multi-peptide-glow-serum',
 'description': 'A multi-peptide concentration fused with 5% Niacinamide and triple molecular weight Hyaluronic Acid to intensely hydrate, firm skin texture, and restore youthful luminescence.',
 'specifications': json.dumps({
 'Key Ingredients': 'Matrixyl 3000, Argireline, 5% Niacinamide, HA',
 'Volume': '50 ml / 1.7 fl. oz.',
 'Skin Types': 'All Skin Types (Dermatologist Tested)',
 'Cruelty Free': '100% Vegan & Leaping Bunny Certified'
 }),
 'price': Decimal('2499.00'),
 'discount_price': Decimal('1699.00'),
 'main_image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=80',
 'stock': 50,
 'rating': 4.9,
 'reviews_count': 188,
 'is_featured': True,
 'is_trending': True,
 'is_flash_deal': True,
 },
 {
 'category': cat_objs['beauty'],
 'name': 'Botanical Radiance Restorative Face Oil',
 'slug': 'botanical-radiance-restorative-face-oil',
 'description': 'Cold-pressed virgin rosehip, squalane, and marula oils infused with stabilized Vitamin C and botanical CoQ10. Melts instantly without oily residue for a velvety radiant finish.',
 'specifications': json.dumps({
 'Base': 'Cold-Pressed Virgin Rosehip & Golden Jojoba',
 'Active': 'THD Ascorbate (Vitamin C) + CoQ10',
 'Absorption': 'Fast-Absorbing Dry Oil Texture',
 'Size': '30 ml Glass Pipette Dropper'
 }),
 'price': Decimal('2999.00'),
 'discount_price': Decimal('2199.00'),
 'main_image': 'https://images.unsplash.com/photo-1608248597359-bb436329a4a7?w=800&q=80',
 'stock': 32,
 'rating': 4.8,
 'reviews_count': 92,
 'is_featured': False,
 'is_trending': False,
 'is_flash_deal': False,
 },

 # Home & Living
 {
 'category': cat_objs['home-living'],
 'name': 'AuraCloud Ultrasonic Aroma Diffuser',
 'slug': 'auracloud-ultrasonic-aroma-diffuser',
 'description': 'Crafted with a frosted artisan ceramic cover and natural bamboo base. Features ultrasonic cold-mist diffusion, warm ambient halo nightlight, and whisper-quiet operation under 20dB.',
 'specifications': json.dumps({
 'Material': 'Artisan Handcrafted Ceramic & Sustainable Bamboo',
 'Water Capacity': '300 ml (Up to 12 Hours Runtime)',
 'Coverage Area': 'Up to 400 sq. ft.',
 'Lighting': 'Warm Amber LED Breathing Ambient Glow',
 'Safety': 'BPA-Free with Auto Waterless Shut-Off'
 }),
 'price': Decimal('3999.00'),
 'discount_price': Decimal('2499.00'),
 'main_image': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&q=80',
 'stock': 28,
 'rating': 4.9,
 'reviews_count': 156,
 'is_featured': True,
 'is_trending': True,
 'is_flash_deal': False,
 },
 {
 'category': cat_objs['home-living'],
 'name': 'ErgoPosture Zero-Gravity Executive Chair',
 'slug': 'ergoposture-zero-gravity-executive-chair',
 'description': 'Engineered with dynamic 3D lumbar support, breathable German elastomeric mesh, 4D adjustable armrests, and synchro-tilt mechanism with multi-position lock for unmatched all-day spinal support.',
 'specifications': json.dumps({
 'Material': 'Breathable Hybrid Elastomeric Tension Mesh',
 'Lumbar Support': 'Self-Adaptive Dynamic 3D Spinal Arch',
 'Mechanism': 'Synchro-Tilt Recline with Multi-Angle Lock',
 'Armrests': '4D (Height, Angle, Depth, Width Adjustable)',
 'Max Load': '150 kg (BIFMA Certified Class 4 Gas Lift)'
 }),
 'price': Decimal('24999.00'),
 'discount_price': Decimal('18999.00'),
 'main_image': 'https://images.unsplash.com/photo-1580481077195-c3a821a58875?w=800&q=80',
 'stock': 15,
 'rating': 4.8,
 'reviews_count': 77,
 'is_featured': True,
 'is_trending': False,
 'is_flash_deal': False,
 },
 {
 'category': cat_objs['home-living'],
 'name': 'Nordic Hand-Thrown Ceramic Fluted Vase',
 'slug': 'nordic-hand-thrown-ceramic-fluted-vase',
 'description': 'Individually wheel-thrown from speckled stoneware clay with a matte chalk fluted silhouette. Perfect centerpiece for botanical arrangements or minimalist standalone sculptural accent.',
 'specifications': json.dumps({
 'Material': 'High-Fired Speckled Stoneware Clay',
 'Finish': 'Matte Chalk White Glaze',
 'Dimensions': 'Height 26cm x Diameter 14cm',
 'Waterproof': '100% Water-tight interior'
 }),
 'price': Decimal('1999.00'),
 'discount_price': Decimal('1299.00'),
 'main_image': 'https://images.unsplash.com/photo-1612196808214-b8e1d6145a8c?w=800&q=80',
 'stock': 22,
 'rating': 4.7,
 'reviews_count': 45,
 'is_featured': False,
 'is_trending': False,
 'is_flash_deal': False,
 },

 # Accessories
 {
 'category': cat_objs['accessories'],
 'name': 'Chronos Titanium Minimalist Smartwatch',
 'slug': 'chronos-titanium-minimalist-smartwatch',
 'description': 'Machined from aerospace-grade Grade-5 Titanium with sapphire crystal glass. Features Always-On AMOLED Retina display, ECG heart rate tracking, sleep cycle analysis, and 14-day battery reserve.',
 'specifications': json.dumps({
 'Case': 'Aerospace Grade 5 Titanium + Ceramic Back',
 'Display': '1.43 Ultra-Bright AMOLED (1000 nits)',
                'Glass': 'Scratch-Proof Sapphire Crystal',
                'Sensors': 'Optical PPG, SpO2, Dual-band GPS, Barometer',
                'Water Resistance': '5 ATM / 50 Meters Water Resistant',
                'Battery': 'Up to 14 Days on Typical Use'
            }),
            'price': Decimal('18999.00'),
            'discount_price': Decimal('14999.00'),
            'main_image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80',
            'stock': 20,
            'rating': 4.9,
            'reviews_count': 124,
            'is_featured': True,
            'is_trending': True,
            'is_flash_deal': False,
        },
        {
            'category': cat_objs['accessories'],
            'name': 'Solaris Aviator Polarized Sunglasses',
            'slug': 'solaris-aviator-polarized-sunglasses',
            'description': 'Lightweight stainless steel wireframe fitted with polarized CR-39 lenses offering 100% UVA/UVB protection and anti-reflective interior coating to eliminate harsh glare.',
            'specifications': json.dumps({
                'Frame': 'High-Tensile Surgical Stainless Steel',
                'Lens': 'Category 3 Polarized CR-39 Lens',
                'Protection': '100% UVA / UVB / UV400 Rating',
                'Hinges': 'Flexible Japanese Barrel Hinges'
            }),
            'price': Decimal('3299.00'),
            'discount_price': Decimal('1999.00'),
            'main_image': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&q=80',
            'stock': 30,
            'rating': 4.7,
            'reviews_count': 82,
            'is_featured': False,
            'is_trending': True,
            'is_flash_deal': False,
        },
        {
            'category': cat_objs['accessories'],
            'name': 'Veloce RFID-Blocking Leather Slim Wallet',
            'slug': 'veloce-rfid-blocking-leather-slim-wallet',
            'description': 'Slim bifold crafted from certified vegetable-tanned full-grain leather. Accommodates up to 10 cards and folded bills with integrated aerospace RFID protection against electronic theft.',
            'specifications': json.dumps({
                'Leather': 'Tuscan Full-Grain Vegetable-Tanned Cowhide',
                'Card Capacity': 'Up to 10 Cards + Cash Pocket',
                'Security': 'Integrated RFID / NFC Data Shielding',
                'Thickness': 'Only 8mm when filled'
            }),
            'price': Decimal('1999.00'),
            'discount_price': Decimal('1199.00'),
            'main_image': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&q=80',
            'stock': 45,
            'rating': 4.8,
            'reviews_count': 163,
            'is_featured': False,
            'is_trending': False,
            'is_flash_deal': True,
        },

        # Sports
        {
            'category': cat_objs['sports'],
            'name': 'Velocity Carbon-Plate Pro Running Shoes',
            'slug': 'velocity-carbon-plate-pro-running-shoes',
            'description': 'Designed for speed and marathon endurance. Features an engineered full-length curved carbon fiber propulsion plate sandwiched within ultra-responsive supercritical Pebax foam.',
            'specifications': json.dumps({
                'Plate': 'Full-Length 3D Curved Carbon Fiber Propulsion Plate',
                'Midsole Foam': 'Supercritical Nitrogen-Infused Pebax Foam',
                'Weight': '198g (Men UK 9)',
                'Drop': '8mm Heel-to-Toe Drop',
                'Outsole': 'Continental Wet-Traction Grip Rubber'
            }),
            'price': Decimal('11999.00'),
            'discount_price': Decimal('7999.00'),
            'main_image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80',
            'stock': 26,
            'rating': 4.9,
            'reviews_count': 195,
            'is_featured': True,
            'is_trending': True,
            'is_flash_deal': False,
        },
        {
            'category': cat_objs['sports'],
            'name': 'IronFlex Smart Quick-Adjust Dumbbell Set',
            'slug': 'ironflex-smart-quick-adjust-dumbbell-set',
            'description': 'Replaces 15 individual pairs of dumbbells. Easily switch weights from 2.5 kg to 24 kg with a single turn of the ergonomic knurled dial mechanism.',
            'specifications': json.dumps({
                'Weight Range': '2.5 kg to 24 kg per dumbbell (5 to 52.5 lbs)',
                'Adjustment': 'Single-Turn Knurled Grip Dial System',
                'Plates': 'Laser-Cut Cast Iron with Impact Rubber Shielding',
                'Includes': 'Dual Heavy-Duty Storage Trays'
            }),
            'price': Decimal('16999.00'),
            'discount_price': Decimal('12999.00'),
            'main_image': 'https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?w=800&q=80',
            'stock': 14,
            'rating': 4.8,
            'reviews_count': 110,
            'is_featured': True,
            'is_trending': False,
            'is_flash_deal': False,
        },
        {
            'category': cat_objs['sports'],
            'name': 'Prana Alignment Eco-Grip Yoga Mat',
            'slug': 'prana-alignment-eco-grip-yoga-mat',
            'description': 'Constructed from sustainably harvested organic natural tree rubber with a moisture-wicking polyurethane top layer. Laser-etched alignment guides ensure optimal posture.',
            'specifications': json.dumps({
                'Material': '100% Natural Tree Rubber Base + Non-Slip PU Surface',
                'Thickness': '4.5mm High-Density Joint Cushioning',
                'Dimensions': '185cm x 68cm (Extra Wide & Long)',
                'Grip': 'Ultimate Non-Slip Grip even in Hot Sweat Workouts'
            }),
            'price': Decimal('3499.00'),
            'discount_price': Decimal('2199.00'),
            'main_image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&q=80',
            'stock': 35,
            'rating': 4.7,
            'reviews_count': 68,
            'is_featured': False,
            'is_trending': False,
            'is_flash_deal': False,
        }
    ]

    created_products = []
    for pdata in products_data:
        p, _ = Product.objects.update_or_create(
            slug=pdata['slug'],
            defaults=pdata
        )
        created_products.append(p)
    print(f✓ Seeded {len(created_products)} high-detail products)

    # 5. Seed sample reviews
    sample_reviews = [
        (Exceptional sound quality and ANC!, The noise cancellation on these headphones rival Sony and Apple at a fraction of the cost. The battery easily lasts a whole work week on a single charge., 5),
        (Best purchase of the year, Build quality is unbelievable. Aluminum frame and switches feel buttery smooth. Typing code has never been this satisfying., 5),
        (Super clear display for development, Colors pop and 4K text sharpness is pristine. USB-C 90W single cable connection to my laptop makes desk setup totally wire-free., 5),
        (Skin feels refreshed within 3 days, Lightweight, non-sticky and gave an instant radiant finish. Truly impressed with the ingredient formulation., 4),
        (Incredible comfort for running, The carbon fiber plate propels you forward effortlessly. Ran my best 10k pace in these shoes last Sunday!, 5)
    ]

    for idx, (title, comment, rating) in enumerate(sample_reviews):
        if idx < len(created_products):
            Review.objects.get_or_create(
                product=created_products[idx],
                user=demo_user,
                defaults={
                    'title': title,
                    'comment': comment,
                    'rating': rating
                }
            )
    print(✓ Seeded sample customer reviews)

    # 6. Seed Demo Orders for john_doe
    if Order.objects.filter(user=demo_user).count() == 0:
        # Order 1: Shipped
        order1 = Order.objects.create(
            order_id=NX-892415,
            user=demo_user,
            customer_name=John Doe,
            email=john.doe@example.com,
            phone=+91 98765 43210,
            shipping_address=Flat 402, Skyline Heights, Cyber City,
            city=Bengaluru,
            state=Karnataka,
            pincode=560100,
            payment_method=UPI,
            payment_status=Completed,
            order_status=Shipped,
            subtotal=Decimal('13498.00'),
            discount_amount=Decimal('4000.00'),
            delivery_charge=Decimal('0.00'),
            total_amount=Decimal('13498.00'),
        )
        OrderItem.objects.create(
            order=order1,
            product=created_products[0],
            product_name=created_products[0].name,
            product_image=created_products[0].main_image,
            price=created_products[0].current_price,
            quantity=1
        )
        OrderItem.objects.create(
            order=order1,
            product=created_products[5],
            product_name=created_products[5].name,
            product_image=created_products[5].main_image,
            price=created_products[5].current_price,
            quantity=1
        )

        # Order 2: Delivered
        order2 = Order.objects.create(
            order_id=NX-712034,
            user=demo_user,
            customer_name=John Doe,
            email=john.doe@example.com,
            phone=+91 98765 43210,
            shipping_address=Flat 402, Skyline Heights, Cyber City,
            city=Bengaluru,
            state=Karnataka,
            pincode=560100,
            payment_method=Card,
            payment_status=Completed,
            order_status=Delivered,
            subtotal=Decimal('7999.00'),
            discount_amount=Decimal('4000.00'),
            delivery_charge=Decimal('0.00'),
            total_amount=Decimal('7999.00'),
        )
        OrderItem.objects.create(
            order=order2,
            product=created_products[15],
            product_name=created_products[15].name,
            product_image=created_products[15].main_image,
            price=created_products[15].current_price,
            quantity=1
        )
        print(✓ Seeded demo past orders for john_doe)

    print(\n🎉 NEXORA Database Seed Complete!)
    print(--------------------------------------------------)
    print(Admin: username='admin', password='admin123')
    print(User: username='john_doe', password='password123')
    print(--------------------------------------------------)

if __name__ == '__main__':
    run_seed()
