from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from decimal import Decimal
from .models import Book, Author, Publisher

class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return Book.objects.select_related('author', 'publisher').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_books'] = Book.objects.all().order_by('-created_at')[:3]
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Исправлено: используем Decimal вместо float
        context['discount_price'] = self.object.price * Decimal('0.9')
        return context