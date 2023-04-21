from django.contrib import admin

from .models import Author, Book, Genre, BookInstance


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    # readonly_fields = ('id',)
    # can_delete = False


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_id', 'display_genre', 'get_author_lname')
    search_fields = ('author_id__last_name',)
    inlines = [BookInstanceInline]

    def get_author_lname(self, obj):
        return obj.author_id.last_name

    get_author_lname.short_description = "Autoriaus pavardė"


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'reader', 'status', 'due_back')
    list_editable = ('reader', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    search_fields = ('id', 'book_id__title')  # book_id - FK iš BookInstance į Book, title - book laukas
    # pagal kurį norime ieškoti abu laukai jungiami __

    fieldsets = (
        ('Bendra info', {'fields': ('id', 'book_id')}),
        ('Prieinamumas', {'fields': ('status', 'due_back', 'reader')})
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
