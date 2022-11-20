# Проект YaMDb

## Технологии
В разработке данного проекта использовался Python в паре с фреймворком Django. База данных PostgresSQL. В качестве веб-сервера используется Gunicorn для передачи данных приложению и Nginx для передачи статики. Весь проект в данный момент разворачивается через Docker из созданных образов.  

## Описание


Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка.

Произведению может быть присвоен жанр (Genre) из списка предустановленных. Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв. 
  

## Пользовательские роли

  

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.

- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.

- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.

- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

- Суперюзер Django — обладет правами администратора (admin).

  

## Ресурсы API YaMDb

  

- Ресурс auth: аутентификация.

- Ресурс users: пользователи.

- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»).

- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.

- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

  

## Установка

  

- Клонируйте новый репозиторий себе на компьютер:

```

git clone git@github.com:DevRomFromDom/infra_sp2.git

```

  

- Перейдите из корневой директории в папку infra:

```

cd infra_sp2/infra

```


Создайте в данной папке .env файл со следующим содержанием:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=123456789  # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

# Стандартные настройки для django
ALLOWED_HOSTS = ['*']
DEBUG = False 
SECRET_KEY = 'super%difficult%key%1233456789'  #Установите свой ключ и держите его в секрете!
```
Используя docker-compose соберите проект из образа, база данных и веб-сервер установятся автоматически: 
```

docker-compose up -d --build

```
После запуска образов необходимо выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создайте суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Скопируйте статику в проект:

```

docker-compose exec web python manage.py collectstatic --no-input

```

Проект запущен и должен быть доступен на http://localhost/
В админку можно попасть через http://localhost/admin/

Для создания резервной копии базы данных используйте:
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
Для загрузки данных в базу из ново-созданного проекта, скопируйте резервную копию в корень проекта:
```
docker-compose cp fixtures.json web:/app - копирование файла из папки infra в корень приложения (контейнера). 
```
Необходимо отчистить существующие данные, для этого выполните следующие команды :
```
docker-compose exec web python manage.py shell
>>>from django.contrib.contenttypes.models import ContentType
>>>> ContentType.objects.all().delete()
>>>> quit()
```
Выполните копирование данных из файла в пустую базу:
```
docker-compose exec web python manage.py loaddata fixtures.json
```

##### Выполните для остановки проекта

```
docker-compose down -v 
```

  

## Авторы

  

- [Григорий Давыдовский](https://github.com/lefaur)

- [Роман Каменских](https://github.com/DevRomFromDom) 

- [Евгений Пермяков](https://github.com/Dexie7)

![example workflow](https://github.com/DevRomFromDom/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
