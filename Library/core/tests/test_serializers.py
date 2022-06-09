import pytz
from django.conf import settings
from django.test import TestCase

from ..models import Books, Authors, Comments
from ..serializers import BookSerializer, AuthorsSerializer, BooksSerializer

time_zone = pytz.timezone(settings.TIME_ZONE)


class BookSerializerTest(TestCase):
    def test_book_serializer_ok(self):
        book_1 = Books.objects.create(title='Книга 1', year=1980)
        book_2 = Books.objects.create(title='Книга 2', year=1990)
        author_1 = Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)
        author_2 = Authors.objects.create(surname='Иванов', name='Иван', patronymic='Иванович', year=1980)

        book_1.authors.add(author_1)
        book_1.save()
        book_2.authors.add(author_1)
        book_2.authors.add(author_2)
        book_2.save()

        serializer_data = BookSerializer([book_1, book_2], many=True).data
        expect_data = [
            {
                'id': book_1.id, 'title': 'Книга 1', 'year': 1980,
                'authors': [
                    {'surname': 'Петров', 'name': 'Пётр', 'patronymic': 'Петрович', 'year': 1976}
                ]
            },
            {
                'id': book_2.id, 'title': 'Книга 2', 'year': 1990,
                'authors': [
                    {'surname': 'Петров', 'name': 'Пётр', 'patronymic': 'Петрович', 'year': 1976},
                    {'surname': 'Иванов', 'name': 'Иван', 'patronymic': 'Иванович', 'year': 1980}
                ]
            }
        ]
        self.assertEqual(expect_data, serializer_data)


class AuthorsSerializerTest(TestCase):
    def test_authors_serializer_ok(self):
        author_1 = Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)
        serializer_data = AuthorsSerializer(author_1, many=False).data
        expect_data = {'surname': 'Петров', 'name': 'Пётр', 'patronymic': 'Петрович', 'year': 1976}
        self.assertEqual(expect_data, serializer_data)


class BooksSerializerTest(TestCase):
    def test_books_serializer_ok(self):
        book_1 = Books.objects.create(title='Книга 1', year=1980)
        book_2 = Books.objects.create(title='Книга 2', year=1990)
        author_1 = Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)
        author_2 = Authors.objects.create(surname='Иванов', name='Иван', patronymic='Иванович', year=1980)

        book_1.authors.add(author_1)
        book_1.save()
        book_2.authors.add(author_1)
        book_2.authors.add(author_2)
        book_2.save()

        comment_1 = Comments.objects.create(content='Комментарий 1, к книге 1', book=book_1)
        comment_2 = Comments.objects.create(content='Комментарий 1, к книге 2', book=book_2)
        comment_3 = Comments.objects.create(content='Комментарий 2, к книге 2', book=book_2)

        serializer_data = BooksSerializer([book_1, book_2], many=True).data

        expect_data = [
            {
                'id': book_1.id, 'title': 'Книга 1', 'year': 1980,
                'authors': ['Петров Пётр Петрович'],
                'comments': [
                    {'id': comment_1.id,
                     'time_creation': comment_1.time_creation.astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S'),
                     'content': 'Комментарий 1, к книге 1'}
                ]
            },
            {
                'id': book_2.id, 'title': 'Книга 2', 'year': 1990,
                'authors': ['Петров Пётр Петрович', 'Иванов Иван Иванович'],
                'comments': [
                    {'id': comment_2.id,
                     'time_creation': comment_2.time_creation.astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S'),
                     'content': 'Комментарий 1, к книге 2'},
                    {'id': comment_3.id,
                     'time_creation': comment_3.time_creation.astimezone(time_zone).strftime('%Y-%m-%d %H:%M:%S'),
                     'content': 'Комментарий 2, к книге 2'},
                ]
            }
        ]
        self.assertEqual(expect_data, serializer_data)
