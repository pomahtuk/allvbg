# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class OrdersList(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь')
    sum = models.CharField(max_length=50, verbose_name='Сумма')
    date = models.DateTimeField('Дата платежа')
    lng = models.CharField(max_length=255, verbose_name='Комментарий', null=True, blank=True)

    def __unicode__(self):
        return self.lng

