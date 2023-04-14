from django.contrib import admin

from .models import Author, Book, Genre, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_id', 'display_genre')
    inlines = [BookInstanceInline]


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'status', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Bendra info', {'fields': ('id', 'book_id')}),
        ('Prieinamumas', {'fields': ('status', 'due_back')})
    )


admin.site.register(Author)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
