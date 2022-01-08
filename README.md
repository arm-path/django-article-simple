# Блог статей.

### О проекте:

Реализован в учебных целях после прохождения учебных видео курсов, и прочтения учебных материалов. 
Один из первых самостоятельных проектов с использованием Django.

### Функционал:

1. Регистрация и авторизация пользователей.
2. Создание разделов, категории к разделам и темы к категориям.
3. Представление список статей по разделам, категориям и темам. Детальное представление статьии
4. Обратная связь.

### Использованы:

Django Debug Toolbar, ckeditor, captcha

### Начало работы:

#### 1. Установить зависимости:

> pip install -r requirements.txt

#### 2. Применить миграции и создать пользователя:

> python manage.py makemigrations \
> python manage.py migrate \
> python manage.py createsuperuser \
> python manage.py collectstatic

#### 3. Запустить Django.

> python manage.py runserver

#### 4. Для работы "Обратной связи"

> > Изменить в файле settings.py: EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
> EMAIL_HOST_PASSWORD.\
> Добавить данные: Файл views.py функция feedback: EMAIL отправителя и получателей.