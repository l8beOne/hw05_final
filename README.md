# Social Network Yatube
<h1 align="center"><img src="https://i.gifer.com/4IS9.gif" height="300" width="400"/></h1>

## Описание проекта:
Создание сайте социальной сети "Yatube"
Она позволяет авторизоваться, добавлять собственный записи, следить за разными авторами(подписываться и отписываться от них). Регистрация реализована с верификацией данных, сменой и восстановлением пароля через email. Присутствует пагинация постов и кэширование. Написаны тесты, проверяющие работу сервиса.
## Стек и Технологии:
* Python 3.9.10
* Django 3.2
* Bootstrap
* Unittest
* pytest
## Как запустить проект:
Склонируйте репозиторий:

```
git clone git@github.com:l8beOne/hw05_final.git
```

Установите и активируйте виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейдите в папку api_yamdb/api_yamdb и примените миграции.

```
python manage.py migrate
```

Запустите проект:

```
python manage.py runserver
```
