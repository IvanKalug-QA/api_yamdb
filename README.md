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
