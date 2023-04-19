from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index_n'),
    path("authors/", views.authors, name='authors_n'),
    path("authors/<int:author_id>", views.author, name='author_n'),
    path("books/", views.BookListView.as_view(), name='books_n'),
    path("books/<int:pk>", views.BookDetailView.as_view(), name='book-detail_n'),
    path("search/", views.search, name='search_n')
]