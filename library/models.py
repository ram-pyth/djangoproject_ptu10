from django.db import models


# Create your models here.
class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=100)
    last_name = models.CharField("Pavardė", max_length=100)

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


class Genre(models.Model):
    name = models.CharField("Žanro pavadinimas", max_length=50, help_text="Įveskite žanrą")

    def __str__(self):
        return f"{self.name}"
