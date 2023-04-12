from django.db import models


# Create your models here.
class Author(models.Model):
    first_name = models.CharField("Vardas", max_length=100)
    last_name = models.CharField("Pavardė", max_length=100)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
