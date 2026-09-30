from django.contrib import admin
from .models import (
    Category, Product, ProductImage, Cart, CartItem,
    Order, OrderItem, Wishlist, Review, UserAddress
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'rating', 'is_featured', 'is_trending', 'is_flash_deal')
    list_filter = ('category', 'is_featured', 'is_trending', 'is_flash_deal')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'line_total')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'email', 'order_status', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('order_status', 'payment_method', 'created_at')
    search_fields = ('order_id', 'customer_name', 'email', 'phone')
    inlines = [OrderItemInline]
    list_editable = ('order_status',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'total_items', 'final_total', 'updated_at')
    inlines = [CartItemInline]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'state', 'pincode', 'is_default')
    search_fields = ('user__username', 'full_name', 'city', 'pincode')
