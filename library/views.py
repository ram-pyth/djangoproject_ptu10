from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Book, BookInstance, Author


def index(request):
    # suskaičiuojam eilutes kiekvienoje lentelėje
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    # žodynas skirtas duomenų perdavimui į šabloną
    data = {
        'num_books_cntx': num_books,
        'num_instances_cntx': num_instances,
        'num_authors_cntx': num_authors,
        'num_inst_avail_cntx': num_instances_available
    }

    return render(request, 'index.html', context=data)


def authors(request):
    # išrenkam visus autorius iš authors lentelės
    authors = Author.objects.all()

    # žodynas skirtas duomenų perdavimui į šabloną
    data = {
        'authors_cntx': authors
    }

    return render(request, 'authors.html', context=data)


def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    data = {
        'author_cntx': single_author
    }
    return render(request, 'author.html', context=data)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # konteksto kintamasis, pavadinimas yra defaultinis
    # formuojamas iš modelio ir generis klasės pavadinimų
    # kodas veiktų ir be šios eilutės
    template_name = "book_list.html"
