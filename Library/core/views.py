from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from .models import Books, Authors, Comments
from .serializers import BooksSerializer, BookSerializer, AuthorsReadSerializer, AuthorsWriteSerializer, \
    CommentsListSerializer, CommentsWriteSerializer


class BookDetailView(DetailView):
    """
    Страница просмотра книги.
    /lib/book/<int:pk>/
    Данные комментариев подтягиваются ajax-запросом со страницы
    """
    model = Books

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Authors.objects.filter(books=self.object)
        context['book_id'] = self.object.pk
        context['menu_link_1'] = {'link': reverse('books_list'), 'name': 'Список книг'}
        return context


def books_list(request):
    """
    "Главная страница" (Перечень книг)
    /lib/books/
    """
    context = {'title': 'Библиотка ;-)'}
    return render(request, 'core/books_list.html', context)


class CommentsAPIList(generics.ListCreateAPIView):
    """
    Список комментариев (GET)
    /lib/api/comments/<int:book_id>/
    Создание комментария (POST)
    /lib/api/comments/
    Для добавления комментария нужно отослать POST вида:
    {
       "content": "Комментарий.... ",
        "book": 13 (id книги)
    }
    """
    queryset = Comments.objects.all().order_by('-time_creation')
    serializer_class = CommentsListSerializer
    authentication_classes = []

    def post(self, request):
        serializer = CommentsWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_queryset(self):
        """
        Если в запросе отсутствует book_id выдаётся список всех комментариев
        """
        book_id = self.kwargs.get('book_id', None)
        if book_id:
            return self.queryset.filter(book__id=book_id)
        else:
            return self.queryset.all()


class CommentAPI(generics.RetrieveAPIView):
    """
    Полный комментарий (GET)
    /lib/api/comment/<pk>/
    """
    queryset = Comments.objects.all()
    serializer_class = CommentsListSerializer


class BooksListPagination(PageNumberPagination):
    """
    Пагинация списка книг
    """
    page_size = 3

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'pagenum': int(self.request.query_params.get('page', 1)),
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class BooksAPIList(generics.ListCreateAPIView):
    """
    Получение списка книг (GET).
    Создание книги (POST).
    /lib/api/books/

    Для создания "книги" необходим JSON вида:
    {
        "title": "Геном",
        "year": 1999,
        "authors": [
            {
                "surname": "Лукьяненко",
                "name": "Сергей",
                "patronymic": "Васильевич"
            }
        ]
    }
    Массив authors можно оставить пустым, если автор не найден в БД, будет создан
    """
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    pagination_class = BooksListPagination

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class BookAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Подробная информация о книге (GET)
    Удаление книги (DELETE)
    Обновление книги (PUT)
    /lib/api/book/<pk>/
    """
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

    def put(self, request, *args, **kwargs):
        """
        Обновление информации о книге.
        Принимает PUT вида:
        {
            "title": "Чёрное копьё.",
            "year": 1992,
            "authors": [
                {
                    "surname": "Перумов",
                    "name": "Николай",
                    "patronymic": "Даниилович"
                }
            ]
        }
        Меняет связь КНИГА - АВТОР. Если пришёл пустой массив "authors" связи КНИГА-АВТОР затронуты не будут.
        Если автор не найден в БД, будет создан
        """
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        authors_data = serializer.validated_data.get('authors', None)

        book_pk = kwargs.get('pk', None)
        books = Books.objects.filter(pk=book_pk)
        if not books:
            raise Http404

        books.update(title=request.data['title'], year=request.data['year'])

        # Обрабатываем полученную информацию об авторах
        # Связанные поля изменяем только если они пришли, если пришёл пустой массив - оставляем как есть, не трогаем.
        if authors_data:
            # Очистка поля
            books[0].authors.clear()
            for author_data in authors_data:
                # Ищем каждого автора в БД
                list_author_exist = Authors.objects.filter(surname=author_data['surname'],
                                                           name=author_data['name'],
                                                           patronymic=author_data['patronymic'])
                if list_author_exist:
                    # Если автор найден - добавляем
                    for author_exist in list_author_exist:
                        books[0].authors.add(author_exist)
                else:
                    # Если не найден - создаём, добавляем .
                    new_author = Authors.objects.create(**author_data)
                    books[0].authors.add(new_author)
                books[0].save()

        # Возвращаем сериализатор от обновлённой книги.
        serializer = BookSerializer(books[0])
        return Response(serializer.data)


class AutorsAPIList(generics.ListCreateAPIView):
    """
    Получение списка авторов (GET).
    Добавление информации об авторе (POST).
    /lib/api/authors/

    Для создания "автора" необходим JSON вида:
    {
        "surname": "Шушпанов",
        "name": "Аркадий",
        "patronymic": "Николаевич",
        "year": 1976,
        "books": [
            {
                "title": "Школьный Надзор",
                "year": 2013
            }
        ]
    }
    Массив "books" можно оставить пустым. Если "книга" не найдена в БД, будет создана.
    """
    queryset = Authors.objects.all()
    serializer_class = AuthorsReadSerializer

    def post(self, request):
        serializer = AuthorsWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class AuthorAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Подробная информация об авторе (GET)
    Удаление автора (DELETE)
    Обновление информации об авторе (PUT)
    /lib/api/author/<pk>/
    """
    queryset = Authors.objects.all()
    serializer_class = AuthorsReadSerializer

    def put(self, request, *args, **kwargs):
        """
        Обновление информации об авторе.
        Ищем существующую запись, если не нашли - выдаём 404 ошибку. Если нашли - обновляем.
        И смотрим пришла-ли информация о книгах, если пришла - изменяем связи записей.
        Принимает PUT вида
        {
            "surname": "Перумов",
            "name": "Николай",
            "patronymic": "Даниилович",
            "year": 1963,
            "books": [
                {
                    "title": "Не время для драконов.",
                    "year": 1997
                },
                {
                    "title": "Эльфийский клинок",
                    "year": 1993
                }
            ]
        }
        Массив "books" можно оставить пустым, тогда связь с книгами затронута не будет
        """
        serializer = AuthorsWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        books_data = serializer.validated_data.get('books', None)

        author_pk = kwargs.get('pk', None)
        authors = Authors.objects.filter(pk=author_pk)
        if not authors:
            raise Http404

        authors.update(surname=request.data['surname'], name=request.data['name'],
                       patronymic=request.data['patronymic'], year=request.data['year'])

        # В связанном поле изменяем только если что-то пришло,
        # если пришёл пустой массив - оставляем как есть, ничего не трогаем.
        if books_data:
            authors[0].books.clear()
            for book_data in books_data:
                list_book_exist = Books.objects.filter(title=book_data['title'], year=book_data['year'])

                if list_book_exist:
                    for book_exist in list_book_exist:
                        authors[0].books.add(book_exist)
                else:
                    new_book = Books.objects.create(**book_data)
                    authors[0].books.add(new_book)
                authors[0].save()

        serializer = AuthorsWriteSerializer(authors[0])
        return Response(serializer.data)
