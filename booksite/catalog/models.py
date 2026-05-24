from django.db import models
from django.urls import reverse
from datetime import date

class Author(models.Model):
    name = models.CharField('Имя автора', max_length=100)
    bio = models.TextField('Биография', blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Publisher(models.Model):
    name = models.CharField('Издательство', max_length=100)
    city = models.CharField('Город', max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'

class Book(models.Model):
    title = models.CharField('Название', max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='books')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    publication_date = models.DateField('Дата публикации')
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    pages = models.IntegerField('Количество страниц')
    cover = models.ImageField('Обложка', upload_to='covers/', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def is_new(self):
        """Проверка, новая ли книга (за последние 30 дней)"""
        delta = date.today() - self.publication_date
        return delta.days <= 30
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-publication_date']