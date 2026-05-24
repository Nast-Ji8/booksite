from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Customer, Product, Cart, CartItem

# Для первого задания (товары/книги)
class BookListView(ListView):
    model = Product
    template_name = 'catalog/book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return Product.objects.all()

class BookDetailView(DetailView):
    model = Product
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'


# Для второго задания (корзины)
class CartListView(ListView):
    """Страница /carts/ - список всех корзин"""
    model = Cart
    template_name = 'catalog/carts.html'
    context_object_name = 'carts'
    
    def get_queryset(self):
        return Cart.objects.select_related('customer').prefetch_related('products').all()

class CartDetailView(DetailView):
    """Детальная страница корзины"""
    model = Cart
    template_name = 'catalog/cart_detail.html'
    context_object_name = 'cart'