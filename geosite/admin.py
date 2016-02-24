# -*- coding: utf-8 -*-

from geosite.models import *
from django.contrib import admin
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from geosite.widgets import *  # подключаем все свои виджеты
from django import forms  # зависимость для переопределения полей формы в админке
from django.utils.translation import ugettext_lazy as _
from suit_redactor.widgets import RedactorWidget


class FirmAdmin(MPTTModelAdmin, SortableModelAdmin):  # класс для админ-панели фирм
    list_display = (
        'name', 'short', 'map_style', 'isstore', 'pub_date')  # список полей, выводимых в админке
    list_filter = ['published', 'isstore', 'map_style']  # поле, по которому возможна фильрация
    search_fields = ['name']  # поле, по которому возможен поиск
    ordering = ('-id',)  # поле и порядок сортировки
    fieldsets = [  # наборы полей
                   ('Основное',
                    {'fields': ['name', 'alias', 'parent', 'container', 'short', 'description', 'published']}),
                   ('Изображения', {'fields': ['image1', 'image2', 'image3', 'image4']}),
                   ('Карта', {'fields': ['lat', 'lng', 'location', 'map_style']}),
                   ('Магазин', {'fields': ['isstore', 'ecwid'], 'classes': ['collapse']}),
                   ('Магазин', {'fields': ['isstore', 'ecwid'], 'classes': ['collapse']}),
                   ('Мета', {'fields': ['meta_key'], 'classes': ['collapse']}),
                   ('Дата', {'fields': ['pub_date'], 'classes': ['collapse']}),
                   ]

    class form(forms.ModelForm):  # вот этот кусок кода дополняет полее ввода картинки её превьюхой
        class Meta:
            widgets = {
                # 'image1': AdminImageWidget,  # виджет определён в geosite/widgets.py
                # 'image2': AdminImageWidget,
                # 'image3': AdminImageWidget,
                # 'image4': AdminImageWidget,
                'location': LocationWidget,
                'short': RedactorWidget(editor_options={'lang': 'ru'}),
                'description': RedactorWidget(editor_options={'lang': 'ru'}),
            }
            ordering = ['tree_id', 'lft']


# class MyTranslatedFirmAdmin(FirmAdmin, TranslationAdmin):
#     class Media:
#         js = (
#             '/static/modeltranslation/js/force_jquery.js',
#             'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
#             '/static/modeltranslation/js/tabbed_translation_fields.js',
#         )
#         css = {
#             'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
#         }
#     pass

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'short', 'pub_date')
    search_fields = ['name']
    list_filter = ['pub_date']
    ordering = ('-pub_date',)
    fieldsets = [
        ('Основное', {'fields': ['name', 'short', 'description']}),
        ('Мета', {'fields': ['meta_key'], 'classes': ['collapse']}),
        ('Дата', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

    class form(forms.ModelForm):  # вот этот кусок кода дополняет полее ввода картинки её превьюхой
        class Meta:
            widgets = {

                'short': RedactorWidget(editor_options={'lang': 'ru'}),
                'description': RedactorWidget(editor_options={'lang': 'ru'}),
            }



class OrdersListAdmin(admin.ModelAdmin):
    list_display = ('date', 'sum', 'user', 'lng')
    search_fields = ['user', 'date']
    list_filter = ['date', 'user']
    ordering = ('-date',)


# class EventAdmin(TranslationAdmin):
# 	list_display = ('name', 'short', 'start_date', 'end_date')
# 	search_fields = ['name']
# 	list_filter = ['start_date', 'end_date']
# 	ordering = ('-start_date',)
# 	fieldsets = [
# 		('Основное', {'fields': ['name', 'short', 'description']}),
# 		('Дата', {'fields': ['start_date', 'end_date']}),
# 	]
# 	class Media:
# 		js = (
# 			'/static/modeltranslation/js/force_jquery.js',
# 			'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
# 			'/static/modeltranslation/js/tabbed_translation_fields.js',
# 		)
# 		css = {
# 			'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
# 		}

class MapAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')
    search_fields = ['title']
    list_filter = ['title']
    ordering = ('-title',)



admin.site.register(Firm, FirmAdmin)
admin.site.register(Article, ArticleAdmin)
# admin.site.register(Event, EventAdmin)
admin.site.register(MapStyle, MapAdmin)
admin.site.register(OrdersList, OrdersListAdmin)
