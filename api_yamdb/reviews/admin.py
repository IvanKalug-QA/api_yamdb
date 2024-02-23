from django.contrib import admin

from .models import Category, Genre, GenreTitle, Title


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):

    @admin.display(description='Жанр')
    def genre_display(self, obj):
        """Функция для отображения ManyToManyField в list_display"""
        return [genre.name for genre in obj.genre.all()]

    list_display = ('name', 'year', 'category', 'genre_display')
    inlines = (GenreTitleInline,)
    search_fields = ('name',)
    list_filter = ('category', 'year', 'genre')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
