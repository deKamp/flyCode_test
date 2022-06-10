import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Authors, Books, Comments
from ..serializers import AuthorsReadSerializer, AuthorsWriteSerializer, CommentsWriteSerializer, \
    CommentsListSerializer, BookSerializer


class GetAllAutorsListTest(APITestCase):
    def setUp(self):
        author_1 = Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)
        author_2 = Authors.objects.create(surname='Иванов', name='Иван', patronymic='Иванович', year=1980)
        author_3 = Authors.objects.create(surname='Александров', name='Александр', patronymic='Александрович',
                                          year=1980)

        book_1 = Books.objects.create(title='Книга 1', year=1980)
        book_1.authors.add(author_1)
        book_1.save()
        book_2 = Books.objects.create(title='Книга 2', year=1990)
        book_2.authors.add(author_2)
        book_2.authors.add(author_3)
        book_2.save()

    def test_get_all_authors(self):
        response = self.client.get(reverse('get_post_all_authors'))
        authors = Authors.objects.all()
        serializer = AuthorsReadSerializer(authors, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleAuthorTest(APITestCase):
    def setUp(self):
        Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)
        self.author_2 = Authors.objects.create(surname='Иванов', name='Иван', patronymic='Иванович', year=1980)

    def test_get_single_author(self):
        response = self.client.get(reverse('get_del_put_single_author', kwargs={'pk': self.author_2.pk}))
        author = Authors.objects.get(pk=self.author_2.pk)
        serializer = AuthorsReadSerializer(author)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_author(self):
        response = self.client.get(reverse('get_del_put_single_author', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
class PostNewAuthorTest(APITestCase):
    def setUp(self):
        Books.objects.create(title='Книга 2', year=1990)

        self.valid_author = {'surname': 'Шушпанов', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                             'books': []}
        self.valid_author_book = {'surname': 'Иванов', 'name': 'Иван', 'patronymic': 'Иванович', 'year': 1980,
                                  'books': [{'title': 'Книга 1', 'year': 2013}]}
        self.valid_author_book_2 = {'surname': 'Петров', 'name': 'Петр', 'patronymic': 'Петрович', 'year': 1980,
                                    'books': [{'title': 'Книга 2', 'year': 1990}]}

        self.invalid_author = {'surname': '', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                               'books': []}

    def test_create_valid_author(self):
        response = self.client.post(reverse('get_post_all_authors'), data=json.dumps(self.valid_author),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_valid_author_with_book(self):
        response = self.client.post(reverse('get_post_all_authors'), data=json.dumps(self.valid_author_book),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_valid_author_with_book_2(self):
        response = self.client.post(reverse('get_post_all_authors'), data=json.dumps(self.valid_author_book_2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_author(self):
        response = self.client.post(reverse('get_post_all_authors'), data=json.dumps(self.invalid_author),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateAuthorTest(APITestCase):
    def setUp(self):
        self.author_1 = Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)
        self.author_2 = Authors.objects.create(surname='Иванов', name='Иван', patronymic='Иванович', year=1980)

        book_1 = Books.objects.create(title='Книга 1', year=1980)
        book_1.authors.add(self.author_2)
        book_1.save()
        Books.objects.create(title='Книга 3', year=1985)

        self.valid_author = {'surname': 'Шушпанов', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                             'books': []}
        self.invalid_author = {'surname': '', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                               'books': []}
        self.valid_author_book = {'surname': 'Александров', 'name': 'Иван', 'patronymic': 'Иванович', 'year': 1976,
                                  'books': [{'title': 'Книга 2', 'year': 1990}]}
        self.valid_author_book_2 = {'surname': 'Александров', 'name': 'Петр', 'patronymic': 'Иванович', 'year': 1976,
                                    'books': [{'title': 'Книга 3', 'year': 1985}]}

    def test_update_valid_author(self):
        response = self.client.put(reverse('get_del_put_single_author', kwargs={'pk': self.author_1.pk}),
                                   data=json.dumps(self.valid_author), content_type='application/json')

        self.valid_author['id'] = self.author_1.pk
        serializer = AuthorsWriteSerializer(self.valid_author)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_valid_author_book(self):
        response = self.client.put(reverse('get_del_put_single_author', kwargs={'pk': self.author_2.pk}),
                                   data=json.dumps(self.valid_author_book), content_type='application/json')

        self.valid_author_book['id'] = self.author_2.pk
        serializer = AuthorsWriteSerializer(self.valid_author_book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_valid_author_book_2(self):
        response = self.client.put(reverse('get_del_put_single_author', kwargs={'pk': self.author_2.pk}),
                                   data=json.dumps(self.valid_author_book_2), content_type='application/json')

        self.valid_author_book_2['id'] = self.author_2.pk
        serializer = AuthorsWriteSerializer(self.valid_author_book_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_invalid_author(self):
        response = self.client.put(reverse('get_del_put_single_author', kwargs={'pk': self.author_1.pk}),
                                   data=json.dumps(self.invalid_author), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_id(self):
        response = self.client.put(reverse('get_del_put_single_author', kwargs={'pk': 30}),
                                   data=json.dumps(self.valid_author), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostNewBookTest(APITestCase):
    def setUp(self):
        self.author_1 = Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)

        self.valid_book_1 = {'title': 'Книга 1', 'year': 1999, 'authors': []}
        self.valid_book_2 = {'title': 'Книга 2', 'year': 1999,
                             'authors': [{'surname': 'Петров', 'name': 'Пётр', 'patronymic': 'Петрович'}]}
        self.valid_book_3 = {'title': 'Книга 3', 'year': 1990,
                             'authors': [{'surname': 'Иванов', 'name': 'Иван', 'patronymic': 'Иванович'}]}

    def test_create_book_1(self):
        response = self.client.post(reverse('get_post_books'), data=json.dumps(self.valid_book_1),
                                    content_type='application/json')
        created_book = Books.objects.get(title='Книга 1')
        serializer = BookSerializer(created_book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_2(self):
        response = self.client.post(reverse('get_post_books'), data=json.dumps(self.valid_book_2),
                                    content_type='application/json')
        created_book = Books.objects.get(title='Книга 2')
        serializer = BookSerializer(created_book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Authors.objects.all().count(), 1)

    def test_create_book_3(self):
        response = self.client.post(reverse('get_post_books'), data=json.dumps(self.valid_book_3),
                                    content_type='application/json')
        created_book = Books.objects.get(title='Книга 3')
        serializer = BookSerializer(created_book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Authors.objects.all().count(), 2)


class CreateCommentTest(APITestCase):
    def setUp(self):
        self.book_1 = Books.objects.create(title='Книга 1', year=1980)
        book_2 = Books.objects.create(title='Книга 2', year=1990)

        self.valid_comment = {'content': 'Комментарий к книге 1.... ', 'book': self.book_1.pk}
        self.invalid_comment = {'content': '', 'book': book_2.pk}

    def test_create_valid_comment(self):
        response = self.client.post(reverse('post_get_comment'), data=json.dumps(self.valid_comment),
                                    content_type='application/json')
        created_comment = Comments.objects.get(book=self.book_1)
        serializer = CommentsWriteSerializer(created_comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_invalid_comment(self):
        response = self.client.post(reverse('post_get_comment'), data=json.dumps(self.invalid_comment),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetCommentsTest(APITestCase):
    def setUp(self):
        self.book_1 = Books.objects.create(title='Книга 1', year=1980)
        book_2 = Books.objects.create(title='Книга 2', year=1990)

        self.comment_1 = Comments.objects.create(content='Комментарий 1 книга 1', book=self.book_1)
        self.comment_2 = Comments.objects.create(content='Комментарий 2 книга 1', book=self.book_1)
        self.comment_3 = Comments.objects.create(content='Комментарий 3 книга 2', book=book_2)

    def test_get_comments(self):
        response = self.client.get(reverse('get_comments', kwargs={'book_id': self.book_1.pk}),
                                   content_type='application/json')
        serializer = CommentsListSerializer([self.comment_2, self.comment_1], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_comments(self):
        response = self.client.get(reverse('post_get_comment'), content_type='application/json')
        comments = Comments.objects.all().order_by('-time_creation')
        serializer = CommentsListSerializer(comments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


