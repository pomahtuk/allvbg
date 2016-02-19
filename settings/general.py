import os

ROOT_PATH = os.path.dirname(__file__)

DEBUG = True
# DEBUG = False
# TEMPLATE_DEBUG = DEBUG

USE_I18N = True

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^^dirc^_ctl=7w39yq4+%47$kbn3xth7%$(6b=njd7!cpzluz4'

CACHE_MIDDLEWARE_SECONDS = 60

ALLOWED_HOSTS = ['geosite.ru', '*.geosite.ru', 'www.geosite.ru']

ADMINS = (
    ('PMaN', 'pman89@yandex.ru'),
)

MANAGERS = ADMINS

INTERNAL_IPS = (
    '127.0.0.1'
)

ROOT_URLCONF = 'urls'

AUTH_PROFILE_MODULE = 'geosite.models.UserProfile'

YANDEX_MAP_KEY = "AK8Ikk0BAAAAdOLMOgIAjpzOBoj6rXFSZEs52f88oUaPYDAAAAAAAAAAAAB3amaZkCtWNLQzxgaVFWYr-ymltQ==~AFuUaU4BAAAA_nfgKgIA-66Q4jxwCOFrx2v8U1aa6UzHDrYAAAAAAAAAAADAFR7JmJumtVbHoQjeteNT2GZJjA==~AFuUaU4BAAAA_nfgKgIA-66Q4jxwCOFrx2v8U1aa6UzHDrYAAAAAAAAAAADAFR7JmJumtVbHoQjeteNT2GZJjA=="

MPTT_ADMIN_LEVEL_INDENT = 20
