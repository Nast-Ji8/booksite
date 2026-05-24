from django import template
from datetime import datetime
from decimal import Decimal

register = template.Library()

# КАСТОМНЫЕ ФИЛЬТРЫ
@register.filter(name='price_format')
def price_format(value):
    """Форматирует цену в рубли"""
    try:
        return f"{float(value):.2f} ₽"
    except (ValueError, TypeError):
        return value

@register.filter(name='truncate_chars')
def truncate_chars(value, max_length):
    """Обрезает строку по количеству символов"""
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value

@register.filter(name='book_age')
def book_age(publication_date):
    """Возвращает возраст книги в годах"""
    from datetime import date
    today = date.today()
    age = today.year - publication_date.year
    if today.month < publication_date.month or (today.month == publication_date.month and today.day < publication_date.day):
        age -= 1
    return age

@register.filter(name='stars_rating')
def stars_rating(rating):
    """Преобразует рейтинг в звезды"""
    try:
        rating = int(rating)
        full_stars = '★' * rating
        empty_stars = '☆' * (5 - rating)
        return full_stars + empty_stars
    except (ValueError, TypeError):
        return '☆☆☆☆☆'

# КАСТОМНЫЕ ТЕГИ
@register.simple_tag
def current_year():
    """Возвращает текущий год"""
    return datetime.now().year

@register.simple_tag
def book_count():
    """Возвращает количество товаров (продуктов) в БД"""
    from catalog.models import Product  # ИСПРАВЛЕНО: Book -> Product
    return Product.objects.count()

@register.simple_tag(takes_context=True)
def active_class(context, url_name):
    """Подсвечивает активную ссылку"""
    request = context.get('request')
    if request and hasattr(request, 'resolver_match') and request.resolver_match:
        if request.resolver_match.url_name == url_name:
            return 'active'
    return ''

@register.inclusion_tag('catalog/_book_card.html')
def book_card(book, show_price=True):
    """Включаемый шаблон для карточки товара"""
    return {
        'book': book,
        'show_price': show_price,
    }

@register.simple_tag
def get_featured_books(limit=3):
    """Возвращает избранные товары (последние добавленные)"""
    from catalog.models import Product  # ИСПРАВЛЕНО: Book -> Product
    return Product.objects.all().order_by('-created_at')[:limit]