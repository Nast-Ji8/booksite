from django.contrib import admin
from .models import Customer, Product, Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ['item_total']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'registered_at']
    list_filter = ['registered_at']
    search_fields = ['name', 'email', 'phone']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    list_editable = ['price', 'stock']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total_items', 'total_price_display', 'created_at']
    list_filter = ['status', 'created_at']  # ФИЛЬТРАЦИЯ
    search_fields = ['customer__name', 'customer__email']  # ПОИСК
    inlines = [CartItemInline]
    
    def total_items(self, obj):
        return obj.total_items()
    total_items.short_description = 'Кол-во товаров'  # ОТОБРАЖЕНИЕ КОЛИЧЕСТВА
    
    def total_price_display(self, obj):
        return f"{obj.total_price()} ₽"
    total_price_display.short_description = 'Общая сумма'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'item_total']
    list_filter = ['cart__status']