from django.urls import path
from . import views, api_views

urlpatterns = [
    # Store Pages
    path('', views.home_view, name='home'),
    path('shop/', views.product_list_view, name='product_list'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/confirmation/<str:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('order/track/', views.order_tracking_view, name='order_tracking'),
    path('order/track/<str:order_id>/', views.order_tracking_view, name='order_tracking_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('compare/', views.compare_view, name='compare'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # AJAX & AI APIs
    path('api/cart/add/', api_views.api_cart_add, name='api_cart_add'),
    path('api/cart/update/', api_views.api_cart_update, name='api_cart_update'),
    path('api/cart/remove/', api_views.api_cart_remove, name='api_cart_remove'),
    path('api/wishlist/toggle/', api_views.api_wishlist_toggle, name='api_wishlist_toggle'),
    path('api/compare/toggle/', api_views.api_compare_toggle, name='api_compare_toggle'),
    path('api/search-suggest/', api_views.api_search_suggest, name='api_search_suggest'),
    path('api/ai-assistant/', api_views.api_ai_assistant, name='api_ai_assistant'),
]
