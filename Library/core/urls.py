from django.urls import path

from .views import BooksAPIList, BookAPI, AuthorAPI, AutorsAPIList, CommentsAPIList, CommentAPI, books_list, \
    BookDetailView

urlpatterns = [
    path('api/book/<int:pk>/', BookAPI.as_view()),
    path('api/books/', BooksAPIList.as_view()),
    path('api/author/<int:pk>/', AuthorAPI.as_view(), name='get_del_put_single_author'),
    path('api/authors/', AutorsAPIList.as_view(), name='get_post_all_authors'),
    path('api/comment/<int:pk>/', CommentAPI.as_view()),
    path('api/comments/', CommentsAPIList.as_view()),
    path('api/comments/<int:book_id>/', CommentsAPIList.as_view()),
    path('books/', books_list, name='books_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail')
]
