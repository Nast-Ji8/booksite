from django.contrib import admin
from .models import Customer, Product, Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Инлайн-редактирование товаров прямо в карточке корзины"""
    model = CartItem
    extra = 1
    fields = ['product', 'quantity', 'item_total_display']
    readonly_fields = ['item_total_display']
    
    def item_total_display(self, obj):
        """Вычисляемое поле в инлайне - стоимость позиции"""
        if obj.pk:
            return f"{obj.item_total()} ₽"
        return "-"
    item_total_display.short_description = 'Сумма'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Админ-панель для покупателей"""
    list_display = ['name', 'email', 'phone', 'registered_at']
    list_filter = ['registered_at']
    search_fields = ['name', 'email', 'phone']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для товаров"""
    list_display = ['name', 'price', 'stock', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    list_editable = ['price', 'stock']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админ-панель для корзин"""
    list_display = [
        'id', 
        'customer', 
        'status', 
        'total_items_display', 
        'total_price_display', 
        'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['customer__name', 'customer__email']
    inlines = [CartItemInline]
    date_hierarchy = 'created_at'
    actions = ['mark_as_completed', 'mark_as_cancelled']
    
    def total_items_display(self, obj):
        """Вычисляемое поле: суммарное количество единиц товара"""
        return f"{obj.total_items()} шт."
    total_items_display.short_description = 'Кол-во товаров'
    
    def total_price_display(self, obj):
        """Вычисляемое поле: итоговая стоимость корзины"""
        return f"{obj.total_price()} ₽"
    total_price_display.short_description = 'Общая сумма'
    
    def mark_as_completed(self, request, queryset):
        """Действие: отметить корзины как завершённые"""
        queryset.update(status='completed')
    mark_as_completed.short_description = 'Отметить как завершённые'
    
    def mark_as_cancelled(self, request, queryset):
        """Действие: отметить корзины как отменённые"""
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = 'Отметить как отменённые'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Админ-панель для позиций корзины"""
    list_display = ['cart', 'product', 'quantity', 'item_total_display']
    list_filter = ['cart__status']
    search_fields = ['cart__customer__name', 'product__name']
    
    def item_total_display(self, obj):
        """Вычисляемое поле: стоимость позиции"""
        return f"{obj.item_total()} ₽"
    item_total_display.short_description = 'Сумма'