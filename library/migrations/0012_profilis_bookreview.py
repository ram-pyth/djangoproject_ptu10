# Generated by Django 4.1.1 on 2023-04-25 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("library", "0011_delete_bookreview"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profilis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nuotrauka",
                    models.ImageField(
                        default="profile_pics/default.png", upload_to="profile_pics"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "content",
                    models.TextField(max_length=2000, verbose_name="Atsiliepimas"),
                ),
                (
                    "book_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="library.book"
                    ),
                ),
                (
                    "reviewer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Asiliepimas",
                "verbose_name_plural": "Atsiliepimai",
                "ordering": ["date_created"],
            },
        ),
    ]
