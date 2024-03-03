from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'author',
                    'score',
                    'pub_date',)
    list_filter = ('title',
                   'author',
                   'pub_date',)
    search_fields = ('title__name',
                     'author__username',)
    list_editable = ('score',)


@admin.register(Comment)
class CommentClass(admin.ModelAdmin):

    list_display = ('pub_date', 'text', 'review', 'author', )
    list_filter = ('review', 'author', 'pub_date',)
    list_editable = ('text',)
    search_fields = ('review', 'author', 'pub_date',)
