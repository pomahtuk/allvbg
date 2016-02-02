# -*- coding: utf-8 -*-

from django.db import models
from tinymce import models as tinymce_models


class Article(models.Model):
    # поле "имя" - должно быть уникально.
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    # короткое описание, показывается в отображении списком
    short = tinymce_models.HTMLField(verbose_name='Короткое описание')
    # Полный текст описания фирмы
    description = tinymce_models.HTMLField(verbose_name='Полный текст')
    # ключевые слова
    meta_key = models.CharField(max_length=100, verbose_name='Ключевые слова')
    # дата создания ресурса
    pub_date = models.DateTimeField('Дата публикации')

    def __unicode__(self):
        return self.name
