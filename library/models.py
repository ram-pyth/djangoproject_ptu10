import uuid

from django.db import models


class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=100)
    last_name = models.CharField("Pavardė", max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    title = models.CharField("Pavadinimas", max_length=200)
    summary = models.TextField("Aprašymas", max_length=1000, help_text="Trumpas knygos aprašymas")
    isbn = models.CharField("ISBN",
                            max_length=13,
                            help_text="13 simbolių <a href='https://www.isbn-international.org/"
                                      "content/what-isbn'>ISBN kodas</a>")
    author_id = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    genre_id = models.ManyToManyField("Genre", help_text="Išrinkite žanrą/us šiai knygai")

    def __str__(self):
        return f"{self.title}"

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre_id.all()][:3])

    display_genre.short_description = 'Žanras'


class Genre(models.Model):
    name = models.CharField("Žanro pavadinimas", max_length=50, help_text="Įveskite žanrą")

    class Meta:
        verbose_name = "Žanras"
        verbose_name_plural = "Žanrai"

    def __str__(self):
        return f"{self.name}"


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unikalus ID leidinio kopijai")
    due_back = models.DateField("Bus prieinama", null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Administruojama'),
        ('p', 'Paimta'),
        ('g', 'Galima paimti'),
        ('r', 'Rezervuota')
    )

    status = models.CharField(
        "Statusas",
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text="Leidinio kopijos statusas"
    )
    book_id = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f"{self.id} {self.book_id.title}"
