from django.db import models
from django.utils import timezone

class Customer(models.Model):
    """Покупатель"""
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    address = models.TextField('Адрес', blank=True)
    registered_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Product(models.Model):
    """Товар (книга)"""
    name = models.CharField('Название', max_length=200)
    author = models.CharField('Автор', max_length=200, blank=True)  # Добавить
    publisher = models.CharField('Издательство', max_length=200, blank=True)  # Добавить
    pages = models.IntegerField('Количество страниц', default=0, blank=True)  # Добавить
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    description = models.TextField('Описание', blank=True)
    stock = models.IntegerField('Количество на складе', default=0)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.price} ₽"
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    """Корзина"""
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('processing', 'В обработке'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='carts',
        verbose_name='Покупатель'
    )
    products = models.ManyToManyField(
        Product, 
        through='CartItem',
        related_name='carts',
        verbose_name='Товары'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.product.price * item.quantity for item in self.cart_items.all())
    
    def total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.cart_items.all())
    
    def __str__(self):
        return f"Корзина {self.customer.name} - {self.created_at.strftime('%d.%m.%Y')}"
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-created_at']


class CartItem(models.Model):
    """Позиция в корзине"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    
    def item_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.cart.customer.name} - {self.product.name} x{self.quantity}"
    
    class Meta:
        verbose_name = 'Позиция корзины'
        verbose_name_plural = 'Позиции корзин'