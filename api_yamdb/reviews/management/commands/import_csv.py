import csv
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Genre, GenreTitle, Title,
                            User, Review, Comment)


class Command(BaseCommand):
    help = 'Imports data from a CSV-files into the database'
    MODEL_FILE_RELATION = {
        Category: 'category.csv',
        Genre: 'genre.csv',
        Title: 'titles.csv',
        GenreTitle: 'genre_title.csv',
        User: 'users.csv',
        Review: 'review.csv',
        Comment: 'comments.csv',
    }
    FOREIGN_KEY_FIELDS = ['category', 'author', 'title', 'review']

    def correct_obj_dict(self, row):
        """
        Принимает на вход словарь с данными для создания одного объекта в БД.
        Проверяет ключи Foreignkey-полей, при необходимости добавляет к
        ключу приставку '_id'. Возвращает откорректированный словарь.
        """
        obj_dict = {}
        for key, value in row.items():
            if key in self.FOREIGN_KEY_FIELDS:
                obj_dict[f'{key}' + '_id'] = value
            else:
                obj_dict[key] = value
        return obj_dict

    def import_data_into_db(self):
        """
        Создает объекты в БД на основе данных из CSV-файлов.
        При создании объекта проверяет существующие записи в БД,
        при совпадении id с существующими записями, заменяет в них
        данные на данные из CSV-файлов.
        """
        for model, file in self.MODEL_FILE_RELATION.items():
            with open(
                os.path.join(settings.CSV_FILES_DIR, f'{file}'),
                encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data = self.correct_obj_dict(row)
                    try:
                        obj = model.objects.get(pk=data.get('id'))
                        obj.delete()
                        obj.refresh_from_db()
                    except model.DoesNotExist:
                        model.objects.create(**data)

    def handle(self, *args, **options):
        """
        Выполняет основную логику работы. Вызывает функцию создания объектов
        в БД на основе данных из CSV-файлов. Выводит в консоль информационное
        сообщение.
        """
        self.import_data_into_db()
        self.stdout.write(self.style.SUCCESS(
            'Данные из CSV-файлов импортированы успешно!'
        ))
