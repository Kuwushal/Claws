from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'featured', 'image_preview', 'created']
    list_filter = ['category', 'featured', 'created']
    list_editable = ['price', 'stock', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    fields = ['name', 'slug', 'category', 'price', 'description', 'image', 'image_url', 'available_sizes', 'stock', 'featured']
    
    def image_preview(self, obj):
        if obj.get_image_url():
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.get_image_url())
        return "No Image"
    image_preview.short_description = "Preview"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'payment_method', 'status', 'created']
    list_filter = ['status', 'payment_method', 'created']
    readonly_fields = ['created', 'payment_id']
    search_fields = ['user__username', 'user__email']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'size', 'price']
    list_filter = ['size']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'created']
    readonly_fields = ['created']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'size', 'quantity']
    list_filter = ['size']