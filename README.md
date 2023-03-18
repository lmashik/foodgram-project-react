# Описание проекта Foodgram
привет

Foodgram - онлайн-сервис, позволяющий просматривать и создавать рецепты 
блюд, подписываться на любимых авторов, добавлять рецепты в избранное и 
список покупок.
-------------------------------

## Использованные технологии

- Python 3.7
- Django Rest Framework 3.2.18
- Djoser 2.1.0
- Reportlab 3.6.12
- Postman (графическая программа для тестирования API)
- SQLite

[//]: # ( - Postgres &#40;система управления базами данных&#41;)

[//]: # ( - Docker &#40;программная платформа контейнеризации&#41;)

[//]: # ( - Docker Compose &#40;средство для определения и запуска приложений Docker с несколькими контейнерами&#41;)

[//]: # ( - Nginx &#40;веб-сервер для статики&#41;)

[//]: # ( - Gunicorn &#40;веб WSGI-сервер&#41;)

[//]: # ( - GitHub Actions &#40;сервис автоматизации тестирования, размещения и запуска проекта на сервере&#41;)

-------------------------------

## Запуск проекта

1. Клонируйте репозиторий и перейдите в него в командной строке
```bash
git clone https://github.com/lmashik/foodgram-project-react.git
```

2. Cоздайте и активируйте виртуальное окружение
```bash
python3 -m venv env
```

* Если у вас Linux/macOS

    ```bash
    source env/bin/activate
    ```

* Если у вас windows

    ```bash
    source env/scripts/activate
    ```

4. Обновите pip до последней версии
```bash
python3 -m pip install --upgrade pip
```

5. Перейдите в директорию
```bash
cd backend
```

6. Установите зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```

7. Выполните миграции
```bash
python3 manage.py migrate
```

8. Запустите проект
```bash
python3 manage.py runserver
```
-------------------------------

## Регистрация

Для регистрации необходимо отправить POST запрос к эндпоинту 
http://127.0.0.1:8000/api/users/, передав в теле запроса:

```json
{
  "username": "vasya.pupkin",
  "password": "Qwerty123",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "email": "vpupkin@yandex.ru"
}
```

## Token

### Получение Token
Для получения токена необходимо отправить POST запрос к эндпоинту 
http://127.0.0.1:8000/api/auth/token/login/, передав в теле запроса:

```json
{
  "password": "Qwerty123",
  "email": "vpupkin@yandex.ru"
}
```

При успешном завершении запроса вы получите ответ в формате JSON. 
Пример ответа на запрос получения токена:

```json
{
    "auth_token": "123e7f1736546f36cfaa231efe691233e7e01b2b"
}
```
-------------------------------

## Запросы и ответы

### Формат запроса
Запрос осуществляется посредством протокола HTTP 1.1 на адрес, 
соответствующий ресурсу. HTTP-запросы должны содержать заголовок:
_Authorization: Token <token>_

### Формат ответа
Ответ сервиса представляет собой JSON-документ в кодировке UTF-8, 
содержимое зависит от запроса.

Пример ответа в случае успешного выполнения запроса одного из рецептов 
на эндпоинт http://127.0.0.1:8000/api/recipes/1/:

_HTTP 1.1 200 OK_
```json
{
    "id": 30,
    "tags": [
        {
            "id": 3,
            "name": "ПП",
            "colour": "#E26C2A",
            "slug": "pp"
        }
    ],
    "author": {
        "id": 3,
        "username": "romashka",
        "email": "romashka@test.test",
        "first_name": "Анатолий",
        "last_name": "Иванов",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 1,
            "name": "Картошка",
            "measurement_unit": "кг",
            "amount": 4
        }
    ],
    "is_favorited": false,
    "is_in_shopping_cart": false,
    "name": "Оливье",
    "image": "http://127.0.0.1:8000/media/11.jpg",
    "text": "все смешать",
    "cooking_time": 4
}
```
-------------------------------

## Ресурсы

Ресурс - часть системы, с которой можно работать. В Foodgram 
ресурсами являются: пользователи, теги, ингредиенты, рецепты, 
рецепты избранного, рецепты списка покупок, любимые авторы (подписки).

```
/api/users/ (GET, POST)

/api/users/<user_id>/ (GET)

/api/users/me/ (GET)

/api/users/set_password/ (POST)

/api/users/subscriptions/ (GET)

/api/tags/ (GET)

/api/tags/<tag_id>/ (GET)

/api/ingredients/ (GET)

/api/ingredients/<ingredient_id>/ (GET)

/api/recipes/ (GET, POST)

/api/recipes/<recipes_id>/ (GET, PATCH, DELETE)

/api/recipes/favorites/ (GET)

/api/recipes/download_shopping_cart/ (GET)
```

Для полноценного использования функционала, связанного с рецептами, 
необходимо начать с добавления тегов и ингредиентов в базу, 
так как рецепты не могут быть созданы без них. 
Теги можно добавить через административную часть сервиса, а для 
добавления ингредиентов подготовлена информация в csv-формате, которую 
можно добавить в базу с помощью команды

```bash
python3 manage.py loadingredients_csv
```
из директории с manage.py (backend)

-------------------------------

## Автор

Мария Лапикова  
mashik.mikhaylova@yandex.ru


