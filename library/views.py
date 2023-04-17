from django.shortcuts import render

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
