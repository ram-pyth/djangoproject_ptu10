from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator

from .models import Book, BookInstance, Author


def index(request):
    # suskaičiuojam eilutes kiekvienoje lentelėje
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_authors = Author.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='g').count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    # žodynas skirtas duomenų perdavimui į šabloną
    data = {
        'num_books_cntx': num_books,
        'num_instances_cntx': num_instances,
        'num_authors_cntx': num_authors,
        'num_inst_avail_cntx': num_instances_available,
        'num_visits_cntx': num_visits
    }

    return render(request, 'index.html', context=data)


def authors(request):
    # išrenkam visus autorius iš authors lentelės, supuslapiuojam
    paginator = Paginator(Author.objects.all(), 3)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)

    # žodynas skirtas duomenų perdavimui į šabloną
    data = {
        'authors_cntx': paged_authors
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
    paginate_by = 5  # puslapiavimas, sukuriamas page_obj šablonui ir išdalinimas po 3 objektus(knygas)
    context_object_name = 'book_list'  # konteksto kintamasis, pavadinimas yra defaultinis
    # formuojamas iš modelio ir generis klasės pavadinimų
    # kodas veiktų ir be šios eilutės
    template_name = "book_list.html"


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'  # šios eilutės nereikia, kontexto kintamasis taip pavadinamas
    # automatiškai, pagal model
    template_name = "book_detail.html"


def search(request):
    query_text = request.GET['search_text']
    query_result = Book.objects.filter(
        Q(title__icontains=query_text) |
        Q(summary__icontains=query_text)
    )  # Q objektas, kai reikia sudėtingesnės paieškos su OR sąlyga
    data = {'query_text_cntx': query_text,
            'query_result_cntx': query_result}
    return render(request, "search.html", context=data)
