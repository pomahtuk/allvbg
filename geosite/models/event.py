# -*- coding: utf-8 -*-

from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    short = models.TextField(verbose_name='Короткое описание')
    # Полный текст описания фирмы
    description = models.TextField(verbose_name='Полный текст')
    # дата создания ресурса
    start_date = models.DateTimeField('Дата начала')
    # дата создания ресурса
    end_date = models.DateTimeField('Дата окончания')

    def __unicode__(self):
        return self.name
