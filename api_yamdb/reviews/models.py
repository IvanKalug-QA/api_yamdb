from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validators import validate_year
from api_yamdb.settings import MIN_SCORE, MAX_SCORE


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

USERS_ROOT = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN)
)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Enter a valid username.',
                code='invalid_username'
            )
        ]
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(default='user',
                            blank=True, max_length=25, choices=USERS_ROOT)

    REQUIRED_FIELDS = ['email']

    USERNAME_FIELD = 'username'

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Enter a valid slug',
                code='invalid_slug'
            )
        ]
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Enter a valid slug',
                code='invalid_slug'
            )
        ]
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска', validators=[validate_year])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, verbose_name='Категория')

    class Meta:
        ordering = ('-year',)
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year', 'category'],
                name='unique_name_year_category',
            )
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,
                              verbose_name='Жанр')
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'{self.genre} {self.title}'


class BaseReviewAndComment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True,)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.CASCADE,
                               verbose_name='Автор',)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(BaseReviewAndComment):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='Произведение',)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)],
        verbose_name='Оценка',
    )

    class Meta(BaseReviewAndComment.Meta):
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='author_title_connection'
            )
        ]

        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        def __str__(self):
            to_str = '{text}; {pub_date}; {author}; {title}; {score}'
            return to_str.format(text=self.text,
                                 pub_date=self.pub_date,
                                 author=self.author.username,
                                 title=self.title,
                                 score=self.score,)


class Comment(BaseReviewAndComment):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='отзыв')

    class Meta(BaseReviewAndComment.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        to_str = '{text}; {pub_date}; {author}; {review};'
        return to_str.format(text=self.text,
                             pub_date=self.pub_date,
                             author=self.author.username,
                             review=self.review,)
