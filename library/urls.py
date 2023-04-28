from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index_n'),
    path("authors/", views.authors, name='authors_n'),
    path("authors/<int:author_id>", views.author, name='author_n'),
    path("books/", views.BookListView.as_view(), name='books_n'),
    path("books/<int:pk>", views.BookDetailView.as_view(), name='book-detail_n'),
    path("search/", views.search, name='search_n'),
    path("mybooks/", views.LoanedBooksByUserListView.as_view(), name='my-borrowed_n'),
    path("mybooks/<uuid:pk>", views.BookByUserDetailView.as_view(), name='my-book_n'),
    path("profilis/", views.profilis, name='profilis_n'),
    path("mybooks/new", views.BookByUserCreateView.as_view(), name='my-borrowed-new_n'),
    path("mybooks/<uuid:pk>/update", views.BookByUserUpdateView.as_view(), name='my-book-update_n'),
    path("mybooks/<uuid:pk>/delete", views.BookByUserDeleteView.as_view(), name='my-book-delete_n'),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns = urlpatterns + [
    path("accounts/", include('django.contrib.auth.urls')),
    path("accounts/register/", views.register, name='register_n'),
]