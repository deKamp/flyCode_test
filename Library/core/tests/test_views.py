import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Authors, Books
from ..serializers import AuthorsReadSerializer, AuthorsWriteSerializer


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
        self.author_1 = Authors.objects.create(surname='Петров', name='Пётр', patronymic='Петрович', year=1976)
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
        self.valid_author = {'surname': 'Шушпанов', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                             'books': []}
        self.invalid_author = {'surname': '', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                               'books': []}

    def test_create_valid_author(self):
        response = self.client.post(reverse('get_post_all_authors'), data=json.dumps(self.valid_author),
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

        self.valid_author = {'surname': 'Шушпанов', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                             'books': []}
        self.invalid_author = {'surname': '', 'name': 'Аркадий', 'patronymic': 'Николаевич', 'year': 1976,
                               'books': []}

    def test_update_valid_author(self):
        response = self.client.put(reverse('get_del_put_single_author', kwargs={'pk': self.author_1.pk}),
                                   data=json.dumps(self.valid_author), content_type='application/json')

        self.valid_author['id'] = self.author_1.pk
        serializer = AuthorsWriteSerializer(self.valid_author)
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

