# allvbg

Весь Выборг - геоинформационный портал на основе Django для небольших городов, в которых ещё нет или не планируется 2Gis.

Проект городского каталога организаций с привязкой к картам Яндекса и детальными описаниями организаций. Заведены модели, настроены шаблоны и views, организован простейший поиск, добавлена страница для регионального виджета яндекса, заложена возможность платного редактирования информации о фирмах пользователями, сделана привязка к робокассе. В шаблонах предусмотрена возможность встраивания интернет-магазина через ECWID. Сделана первичная SEO-подготовку: META-теги, ЧПУ, sitemap.

### Используемые пакеты:
* Django
* FeinCMS
* django-admin-tools
* django-debug-toolbar
* django-filebrowser
* django-grappelli
* django-modeltranslation
* django-mptt
* django-ratings
* django-tinymce
* easy-thumbnails
* feedparser

# Установка

Для запуска проекта потребуется хостинг с поддержкой pytnon и Django.

## Настройка приложения

1 Импортируйте sql-файл с демо-данными в базу данных MySQL, созданную под проект.
2 Откройте файл settings.py в каталоге проекта и замените все данные в соответсвующих строчках своими.
Строки, требующие изменений:
```python
PROJECT_PATH = '/var/www/pman/data/www/allvbgru'

ADMINS = (
    ('PMaN', 'pman89@yandex.ru'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'user',
        'PASSWORD': 'password',
    }
}

STATIC_URL = 'http://allvbg.ru/static/'

ST_URL = 'http://allvbg.ru/static/allvbg/'
ST_ROOT = '/var/www/pman/data/www/allvbgru/static/allvbg/'

MEDIA_ROOT = '/var/www/pman/data/www/allvbgru/static/allvbg/'

MEDIA_URL = 'http://allvbg.ru/static/allvbg/'

TINYMCE_JS_URL = 'http://allvbg.ru/static/tiny_mce/tiny_mce_src.js'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/www/pman/data/Django_cache',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
```

## Настройка сервера 

### Если вы пользуетесь shared-хостингом

Обратитесь в службу поддержки хостинга с просьбой объяснить процесс запуска python-приложений и установки дополнительных пакетов.

### При использовании собственного севера

#### Установка пакетов

Зайдите в директорию проекта и выполните команду

`pip install -r requirements.txt`

После успешного выполнения команды все необходимые для работы проекта пакеты будут установлены.

В случае ошибок при устанвки пакетов, а ошибки могут возникнуть при установки PIL и MySQL-python, установите эти пакеты из репозитория вашего дистрибутива, например, для Debian:
```
apt-get install python-imaging
apt-get install python-mysqldb
 ```
 
#### Настройка web-сервера

##### WSGI

Откройте файл django-fcgi и укажите в нём правильный путь до папки, куда был скопирован код проета.

После этого выполните команды:
```
cp ./django-fcgi /etc/init.d/django-fcgi 
chmod +x /etc/init.d/django-fcgi
update-rc.d /etc/init.d/django-fcgi defaults
```

Теперь вы можете запустить приложение командой:

`/etc/init.d/django-fcgi start`

Так же присутсвуют команды stop и restart

Приложение будет запущено на localhost:8881

##### Ngnix

Добавьте в файл настроек nginx (обычно /etc/nginx/nginix.conf) ещё одну секцию.

    server {
      listen #your ip#;
      server_name #your site adress#;
      location /static {
        root #path to project folder#;
      }
      location / {
        root   #path to project folder#;
        index  index.html index.htm;
        fastcgi_pass 127.0.0.1:8881;

        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_param REQUEST_METHOD $request_method;
        fastcgi_param QUERY_STRING $query_string;
        fastcgi_param CONTENT_TYPE $content_type;
        fastcgi_param CONTENT_LENGTH $content_length;
        fastcgi_param REMOTE_PORT $remote_port;
        fastcgi_param SERVER_PROTOCOL $server_protocol;
        fastcgi_param SERVER_PORT $server_port;
        fastcgi_param SERVER_NAME $server_name;
        fastcgi_pass_header Authorization;
        fastcgi_intercept_errors off;
        fastcgi_param REMOTE_ADDR $remote_addr;
      }
    }