from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from .forms import BookReviewForm, UserUpdateForm, ProfilisUpdateForm
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


class BookDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'  # šios eilutės nereikia, kontexto kintamasis taip pavadinamas
    # automatiškai, pagal model
    template_name = "book_detail.html"
    form_class = BookReviewForm

    # nurodome kur pateksim po formos submitinimo
    def get_success_url(self):
        return reverse('book-detail_n', kwargs={'pk': self.object.id})

    # post metodas mūsų pakeistas
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    #
    def form_valid(self, form):
        form.instance.book_id = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


def search(request):
    query_text = request.GET['search_text']
    query_result = Book.objects.filter(
        Q(title__icontains=query_text) |
        Q(summary__icontains=query_text)
    )  # Q objektas, kai reikia sudėtingesnės paieškos su OR sąlyga
    data = {'query_text_cntx': query_text,
            'query_result_cntx': query_result}
    return render(request, "search.html", context=data)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = 'bookinstance_list'  # nebūtina, tokį pavadinimą kontekste django sukuria automatiškai
    template_name = 'user_books.html'
    paginate_by = 5

    def get_queryset(self):
        query = BookInstance.objects.filter(reader=self.request.user).filter(status__exact='p').order_by('due_back')
        return query


class BookByUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookInstance
    template_name = 'user_book.html'


@csrf_protect
def register(request):
    if request.method == "POST":
        # duomenų surinkimas iš register formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # ar sutampa slaptažodžiai
        if password == password2:
            # ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Vartotojo vardas {username} yra užimtas!!!")
                return redirect('register_n')
            else:
                # ar nėra sitemoj tokio pačio emailo
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Jau egzistuoja vartotojas su emailu {email}!!!")
                    return redirect('register_n')
                else:
                    # jei patikrinimai praėjo registruojam naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f"Vartotojas {username} užregistruotas!")
                    return redirect('login')
        else:
            messages.error(request, "Slaptažodžiai nesutampa!!!")
            return redirect('register_n')
    return render(request, "registration/register.html")


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis_n')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    data = {
        'u_form_cntx': u_form,
        'p_form_cntx': p_form,
    }

    return render(request, "profilis.html", context=data)
