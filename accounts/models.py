# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import hashlib
import urllib2
from datetime import *
from geosite.models import Firm
from django.db.models.signals import post_save


from django.contrib.auth.models import User


def create_user_profile(instance, created, **kwargs):
    if created:
        # TODO: move this to settings
        token = "cbe688b751993340999aceaa28432eba44eeb4eb418388e309bbdcb5"
        crc = hashlib.md5(instance.username + str(instance.id) + "someSalT").hexdigest()[:10]
        url = "https://pddimp.yandex.ru/reg_user_token.xml?token=" + token + "&u_login=" + instance.username + "&u_password=" + crc
        result = urllib2.urlopen(url)

        UserProfile.objects.create(user=instance, generated_password=crc,
                                   generated_email=instance.username + "@geosite.ru", paid_till=datetime.now())


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    editor_for = models.ForeignKey(Firm, verbose_name='Редактирует фирму:', null=True, blank=True)
    generated_password = models.CharField(max_length=255, verbose_name='Сгенерированный пароль', null=True, blank=True)
    generated_email = models.CharField(max_length=255, verbose_name='Сгенерированный email', null=True, blank=True)
    paid_till = models.DateTimeField('Оплачено до', null=True, blank=True)

    post_save.connect(create_user_profile, sender=User)
