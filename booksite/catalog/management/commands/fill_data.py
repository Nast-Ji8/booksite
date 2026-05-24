from django.core.management.base import BaseCommand
from catalog.models import Author, Publisher, Book
from datetime import date

class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'
    
    def handle(self, *args, **options):
        # Создаем авторов
        authors = [
            Author.objects.create(name='Лев Толстой', birth_date='1828-09-09'),
            Author.objects.create(name='Фёдор Достоевский', birth_date='1821-11-11'),
            Author.objects.create(name='Джордж Оруэлл', birth_date='1903-06-25'),
        ]
        
        # Создаем издательства
        publishers = [
            Publisher.objects.create(name='Эксмо', city='Москва'),
            Publisher.objects.create(name='АСТ', city='Санкт-Петербург'),
        ]
        
        # Создаем книги
        books_data = [
            ('Война и мир', authors[0], publishers[0], 500, '2020-01-15', '9785171234567', 1300),
            ('Анна Каренина', authors[0], publishers[0], 450, '2021-03-20', '9785171234568', 890),
            ('Преступление и наказание', authors[1], publishers[1], 600, '2019-08-10', '9785171234569', 750),
            ('1984', authors[2], publishers[1], 350, '2023-01-05', '9785171234570', 650),
        ]
        
        for title, author, publisher, pages, pub_date, isbn, price in books_data:
            Book.objects.create(
                title=title,
                author=author,
                publisher=publisher,
                pages=pages,
                publication_date=pub_date,
                isbn=isbn,
                price=price
            )
        
        self.stdout.write(self.style.SUCCESS('Данные успешно добавлены!'))