import json
import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    icon = models.CharField(max_length=50, default='bi-tag', help_text='Icon class or identifier')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def product_count(self):
        return self.products.count()


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    description = models.TextField()
    specifications = models.TextField(
        blank=True,
        default='{}',
        help_text='JSON string or line-separated key: value specs'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Regular price in INR')
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Discounted sale price in INR'
    )
    main_image = models.URLField(max_length=600, help_text='Primary image URL')
    stock = models.PositiveIntegerField(default=15)
    rating = models.FloatField(default=4.5)
    reviews_count = models.PositiveIntegerField(default=0)
    
    # Flags
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_flash_deal = models.BooleanField(default=False)
    flash_deal_end = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        if self.discount_price and self.discount_price > 0 and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def has_discount(self):
        return bool(self.discount_price and self.discount_price > 0 and self.discount_price < self.price)

    @property
    def discount_percentage(self):
        if self.has_discount:
            pct = round(((self.price - self.discount_price) / self.price) * 100)
            return max(1, pct)
        return 0

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def specs_dict(self):
        if not self.specifications:
            return {}
        try:
            return json.loads(self.specifications)
        except Exception:
            parsed = {}
            for line in self.specifications.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    parsed[k.strip()] = v.strip()
            return parsed

    @property
    def full_stars(self):
        return range(int(self.rating))

    @property
    def has_half_star(self):
        return (self.rating - int(self.rating)) >= 0.3

    @property
    def empty_stars(self):
        count = 5 - int(self.rating) - (1 if self.has_half_star else 0)
        return range(max(0, count))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image_url = models.URLField(max_length=600)
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'Image for {self.product.name}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = self.user.username if self.user else f'Guest ({self.session_key})'
        return f'Cart #{self.id} - {owner}'

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += Decimal(str(item.product.price)) * item.quantity
        return total

    @property
    def total_savings(self):
        savings = Decimal('0.00')
        for item in self.items.all():
            if item.product.has_discount:
                diff = Decimal(str(item.product.price)) - Decimal(str(item.product.discount_price))
                savings += diff * item.quantity
        return savings

    @property
    def effective_subtotal(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += Decimal(str(item.product.current_price)) * item.quantity
        return total

    @property
    def delivery_charge(self):
        if self.effective_subtotal > Decimal('999.00') or self.items.count() == 0:
            return Decimal('0.00')
        return Decimal('99.00')

    @property
    def final_total(self):
        return self.effective_subtotal + self.delivery_charge


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'

    @property
    def line_total(self):
        return Decimal(str(self.product.current_price)) * self.quantity

    @property
    def original_line_total(self):
        return Decimal(str(self.product.price)) * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('Placed', 'Order Placed'),
        ('Confirmed', 'Confirmed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'Instant UPI / QR'),
        ('Card', 'Credit / Debit Card'),
        ('NetBanking', 'Net Banking'),
    ]

    order_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, default='UPI')
    payment_status = models.CharField(max_length=30, default='Completed')
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Placed')

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f'NX-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.order_id} - {self.customer_name}'

    @property
    def status_step_index(self):
        steps = {
            'Placed': 1,
            'Confirmed': 2,
            'Packed': 3,
            'Shipped': 4,
            'Delivered': 5,
            'Cancelled': 0,
        }
        return steps.get(self.order_status, 1)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    product_image = models.URLField(max_length=600, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product_name} in {self.order.order_id}'

    @property
    def line_total(self):
        return self.price * self.quantity


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=150)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.rating} star by {self.user.username} for {self.product.name}'

    @property
    def full_stars(self):
        return range(self.rating)

    @property
    def empty_stars(self):
        return range(5 - self.rating)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'User Addresses'

    def __str__(self):
        return f'{self.full_name} ({self.city}, {self.pincode})'
