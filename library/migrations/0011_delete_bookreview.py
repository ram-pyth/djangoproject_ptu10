# Generated by Django 4.1.1 on 2023-04-25 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0010_alter_author_description_alter_book_cover_bookreview"),
    ]

    operations = [
        migrations.DeleteModel(
            name="BookReview",
        ),
    ]
