# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-24 17:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geosite', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_password', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u043f\u0430\u0440\u043e\u043b\u044c')),
                ('generated_email', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u0421\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 email')),
                ('paid_till', models.DateTimeField(blank=True, null=True, verbose_name='\u041e\u043f\u043b\u0430\u0447\u0435\u043d\u043e \u0434\u043e')),
                ('editor_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geosite.Firm', verbose_name='\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u0443\u0435\u0442 \u0444\u0438\u0440\u043c\u0443:')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]