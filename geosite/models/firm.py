from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from tinymce import models as tinymce_models
from map_style import MapStyle
from django.utils.timezone import now as tz_now


class Firm(MPTTModel):
    name = models.CharField(max_length=50, verbose_name='Название')
    alias = models.CharField(max_length=50, unique=True, verbose_name='Псевдоним')

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    container = models.BooleanField(verbose_name='Контейнер?', default=False)

    short = tinymce_models.HTMLField(verbose_name='Короткое описание', null=True, blank=True)
    description = tinymce_models.HTMLField(verbose_name='Полный текст', null=True, blank=True)

    image1 = models.ImageField(upload_to='uploads', verbose_name='Изображение 1', null=True, blank=True)
    image2 = models.ImageField(upload_to='uploads', verbose_name='Изображение 2', null=True, blank=True)
    image3 = models.ImageField(upload_to='uploads', verbose_name='Изображение 3', null=True, blank=True)
    image4 = models.ImageField(upload_to='uploads', verbose_name='Изображение 4', null=True, blank=True)

    meta_key = models.CharField(max_length=100, verbose_name='Ключевые слова', null=True, blank=True)

    location = models.CharField(max_length=100, verbose_name='Адрес', null=True, blank=True)
    lat = models.CharField(max_length=255, verbose_name='Широта', null=True, blank=True)
    lng = models.CharField(max_length=255, verbose_name='Долгота', null=True, blank=True)
    map_style = models.ForeignKey(MapStyle, verbose_name='Стиль на карте', null=True, blank=True)

    isstore = models.BooleanField(verbose_name='Магазин?', default=False)
    ecwid = models.CharField(max_length=50, verbose_name='ID магазина ECWID', null=True, blank=True)
    pub_date = models.DateTimeField('Дата публикации', null=True, blank=True, default=tz_now)

    totalvotes = models.BigIntegerField(verbose_name='Количество проголосовавших', null=True, blank=True)
    raiting = models.FloatField(verbose_name='Рейтинг', null=True)

    published = models.BooleanField(verbose_name='Опубликовано?', default=False)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name
