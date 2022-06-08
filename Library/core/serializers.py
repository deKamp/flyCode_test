from rest_framework import serializers

from .models import Books, Authors, Comments


class BooksWriteSerializer(serializers.ModelSerializer):
    """
    Используется при внесении информации об авторе, если он добавляется сразу с книгами.
    POST /lib/api/author/
    """
    class Meta:
        model = Books
        fields = ('title', 'year')


class AuthorsWriteSerializer(serializers.ModelSerializer):
    """
    Ввод информации об авторе Фамилия, Имя, Отчество, год, книги
    POST /lib/api/author/
    PUT /lib/api/author/<pk>/
    """
    books = BooksWriteSerializer(many=True)

    class Meta:
        model = Authors
        fields = ('id', 'surname', 'name', 'patronymic', 'year', 'books')

    def create(self, validated_data):
        books_data = validated_data.pop('books')
        author = Authors.objects.create(**validated_data)
        for book_data in books_data:
            list_exist_books = Books.objects.filter(title=book_data['title'], year=book_data['year'])
            if list_exist_books:
                for exist_book in list_exist_books:
                    author.books.add(exist_book)
            else:
                new_book = Books.objects.create(**book_data)
                author.books.add(new_book)
        return author


class BooksReadSerializer(serializers.ModelSerializer):
    """
    Вывод информации о книге для списка авторов
    GET /lib/api/authors/
    """
    class Meta:
        model = Books
        fields = ('id', 'title', 'year')


class AuthorsReadSerializer(serializers.ModelSerializer):
    """
    Вывод списка авторов с объединением ФИО в строку
    GET /lib/api/authors/
    """
    full_name = serializers.SerializerMethodField()
    books = BooksReadSerializer(read_only=True, many=True)

    def get_full_name(self, obj):
        return f'{obj.surname} {obj.name} {obj.patronymic}'

    class Meta:
        model = Authors
        fields = ('id', 'full_name', 'year', 'books')


class AuthorsListingField(serializers.RelatedField):
    """
    Выводит имя автора в одну строку в связанном поле
    GET /lib/api/books/
    """
    def to_representation(self, value):
        return f'{value.surname} {value.name} {value.patronymic}'


class CommentsWriteSerializer(serializers.ModelSerializer):
    """
    Используется при записи комментария
    POST /lib/api/comments/
    """

    class Meta:
        model = Comments
        fields = ('id', 'time_creation', 'content', 'book')


class CommentsListSerializer(serializers.ModelSerializer):
    """
    Используется при выводе списка комментариев а также полный комментарий
    GET /lib/api/comments/
    GET /lib/api/comment/<pk>/
    """
    book = BooksReadSerializer(many=False)

    class Meta:
        model = Comments
        fields = ('id', 'time_creation', 'content', 'book')


class CommentsSerializer(serializers.ModelSerializer):
    """
    Используется при выводе информации о книге
    GET /lib/api/books/
    """
    class Meta:
        model = Comments
        fields = ('id', 'time_creation', 'content')


class BooksSerializer(serializers.ModelSerializer):
    """
    Вывод информации о книге с использованием сериализатора об авторе "в одну строку"
    Используется при удалении книги, а также при выводе полной информации
    GET /lib/api/books/
    """
    authors = AuthorsListingField(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Books
        fields = ('id', 'title', 'year', 'authors', 'comments')


class AuthorsSerializer(serializers.ModelSerializer):
    """
    Ввод информации об авторе Фамилия, Имя, Отчество, год
    Используется в классах записи (POST, PUT)
    """
    class Meta:
        model = Authors
        fields = ('surname', 'name', 'patronymic', 'year')


class BookSerializer(serializers.ModelSerializer):
    """
    Запись информации о книге
    POST /lib/api/books/
    PUT /lib/api/book/<pk>/
    """
    authors = AuthorsSerializer(many=True)

    class Meta:
        model = Books
        fields = ('id', 'title', 'year', 'authors')

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        book = Books.objects.create(**validated_data)
        for author_data in authors_data:
            list_author_exist = Authors.objects.filter(surname=author_data['surname'],
                                                       name=author_data['name'],
                                                       patronymic=author_data['patronymic'])
            if list_author_exist:
                for author_exist in list_author_exist:
                    book.authors.add(author_exist)
            else:
                new_author = Authors.objects.create(**author_data)
                book.authors.add(new_author)
        return book
