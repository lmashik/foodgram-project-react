# Foodgram

-------------------------------
## Описание

Foodgram - онлайн-сервис, позволяющий просматривать и создавать рецепты 
блюд, подписываться на любимых авторов, добавлять рецепты в избранное и 
список покупок.

-------------------------------
## Используемые технологии

- Python 3.7
- Django Rest Framework 3.2.18
- Djoser 2.1.0
- Reportlab 3.6.12
- Postman (графическая программа для тестирования API)
- Postgres (система управления базами данных)
- Docker (программная платформа контейнеризации)
- Docker Compose (средство для определения и запуска приложений Docker с несколькими контейнерами)
- Nginx (веб-сервер для статики)
- Gunicorn (веб WSGI-сервер)
- GitHub Actions (сервис автоматизации тестирования, размещения и запуска проекта на сервере)

-------------------------------

## Запуск проекта в контейнерах на своем сервере

1. Клонируйте репозиторий и перейдите в директорию infra в командной строке
```bash
git clone https://github.com/lmashik/foodgram-project-react.git
```

```bash
cd infra/
```
2. В nginx.conf поменяйте IP-адрес и/или домен на свой 

3. Cоздайте файл .env для переменных виртуального окружения 
и заполните его по образцу
```bash
nano .env
```

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=<username>
    POSTGRES_PASSWORD=<password>
    DB_HOST=db
    DB_PORT=5432

4. Создайте и запустите контейнеры
```bash
sudo docker-compose up -d
```
(Для новых версий docker compose как плагина docker
```bash
sudo docker compose up -d
```
)

5. Примените миграции внутри контейнера backend
```bash
sudo docker-compose exec backend python manage.py migrate
```
или
```bash
sudo docker compose exec backend python manage.py migrate
```

6. Соберите статику
```bash
sudo docker-compose exec backend python manage.py collectstatic
```
или
```bash
sudo docker compose exec backend python manage.py collectstatic
```

Проект будет доступен по адресу http://localhost/  
Административная часть — по адресу http://localhost/admin/ 
Для доступа в административную часть создайте суперпользователя
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
или
```bash
sudo docker compose exec backend python manage.py createsuperuser
```

Документация к API — по адресу http://localhost/api/docs/redoc.html

Для полноценного использования функционала, связанного с рецептами, 
необходимо начать с добавления тегов и ингредиентов в базу, 
так как рецепты не могут быть созданы без них. 
Теги можно добавить через административную часть сервиса, а для 
добавления ингредиентов подготовлена информация в csv-формате, которую 
можно добавить в базу с помощью команды

```bash
sudo docker-compose exec backend python manage.py loadingredients_csv
```
или
```bash
sudo docker compose exec backend python manage.py loadingredients_csv
```

-------------------------------

## API

### Запуск

Сервис Foodgram реализован через взаимодействие с API. 
Для запуска backend-части (API Foodgram) проекта:

1. Перейдите в директорию backend, создайте и активируйте виртуальное 
окружение

```bash
cd ../backend
```

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

2. Обновите pip до последней версии
```bash
python3 -m pip install --upgrade pip
```

3. Установите зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```

4. Выполните миграции
```bash
python3 manage.py migrate
```

5. Запустите проект
```bash
python3 manage.py runserver
```

### Регистрация

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

### Token

#### Получение Token
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


### Запросы и ответы

#### Формат запроса
Запрос осуществляется посредством протокола HTTP 1.1 на адрес, 
соответствующий ресурсу. HTTP-запросы должны содержать заголовок:
_Authorization: Token <token>_

#### Формат ответа
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

### Ресурсы

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


