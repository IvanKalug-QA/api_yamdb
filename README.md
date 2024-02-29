## API_YAMDB

### 1. Описание проекта:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число).
Пользователи могут также оставлять комментарии к отзывам.


___

### 2. Авторы проекта:
- Иван Калугин
- Александр Талбутдинов
- Наталья Сурина
___
### 3. Использованные технологии:
- Python 3.9.10
- Django 3.2.16
- DjangoRestFramework 3.12.4
- Git

### 4. Как запустить проект на локальном компьютере:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:IvanKalug-QA/api_yamdb.git
```

```
cd api_yamdb
```

2. Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

3. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4. Перейти в директорию api_yamdb:

```
cd api_yamdb
```

5. Выполнить миграции:

```
python manage.py migrate
```

6. Запустить проект:

```
python manage.py runserver
```
___
### 5. Документация к проекту и примеры запросов:

Когда вы запустите проект, по адресу  http://127.0.0.1:8000/redoc/ будет доступна документация для API_YAMDB. В документации описан полный перечень эндпоинтов, примеров запросов и ответов к ним. Документация представлена в формате Redoc.
___
### 6. Импортирование тестовых данных:

В директории /api_yamdb/static/data, подготовлены несколько файлов в формате CSV с контентом для ресурсов Users, Titles, Categories, Genres, Reviews и Comments.

Данные из CSV-файлов можно импортировать в БД с помощью менеджмент-команды:
```
python manage.py import_csv
```

Логика работы данной менеджмент-команды следующая:

1. В файле '/api_yamdb/reviews/management/commands/import_csv.py' создан class Command.
2. В атрибуте Model_file_relation класса Command записан словарь, в котором в формате ключ-значение указаны Модели и соответствующие им CSV-файлы для импорта данных:
```
class Command(BaseCommand):
    Model_file_relation = {
        Category: 'category.csv',
        Genre: 'genre.csv',
        Title: 'titles.csv',
        GenreTitle: 'genre_title.csv',
        User: 'users.csv',
        Review: 'review.csv',
        Comment: 'comments.csv',
    }
```
3. Порядок моделей важен, так как некоторые модели могут ссылаться на существующие записи в других моделях.
4. Перед созданием объекта в БД поля модели, содержащиеся в CSV-файле, проходят проверку и передаются в откорректированный словарь obj_dict.
5. Если в CSV-файле присутствует поле модели, которое содержит id связанной модели, а название этого поля не содержит приставку '_id', то
в откорректированном словаре obj_dict к названию поля будет добавлена приставка '_id'.
6. Откорректированный словарь obj_dict используется для создания объекта в БД.
7. При создании объекта в БД осуществляется проверка существующих записей в БД. При совпадении id создаваемого объекта с id существующего объекта, существующий объект в БД будет заменен на объект из CSV-файла.
8. После того как команда отработала, в терминал выводится информационное сообщение: 'Данные из CSV-файлов импортированы успешно!'
___
