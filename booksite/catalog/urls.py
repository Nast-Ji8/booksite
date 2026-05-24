from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Для первого задания (книги/товары)
    path('', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    
    # Для второго задания (корзины)
    path('carts/', views.CartListView.as_view(), name='cart_list'),  # ГЛАВНАЯ СТРАНИЦА КОРЗИН
    path('cart/<int:pk>/', views.CartDetailView.as_view(), name='cart_detail'),
]