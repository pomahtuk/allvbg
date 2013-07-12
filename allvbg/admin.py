# -*- coding: utf-8 -*-
from allvbg.models import *
from django.contrib import admin
from feincms.admin import tree_editor
from mptt.admin import MPTTModelAdmin #зависимость для отображения материалов в виде дерева в админке
from allvbg.widgets import *  #подключаем все свои виджеты
from django import forms #зависимость для переопределения полей формы в админке
from modeltranslation.admin import TranslationAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from suit_redactor.widgets import RedactorWidget

class FirmAdmin(tree_editor.TreeEditor): #класс для админ-панели фирм
	list_display = ('name', 'short', 'map_style', 'isstore', 'published_toggle', 'pub_date') #список полей, выводимых в админке
	list_filter = ['published', 'isstore', 'map_style'] #поле, по которому возможна фильрация
	search_fields = ['name'] #поле, по которому возможен поиск
	ordering = ('-id',) #поле и порядок сортировки
	published_toggle = tree_editor.ajax_editable_boolean('published', _('published'))
	fieldsets = [ #наборы полей
		('Основное', {
			'classes': ['suit-tab', 'suit-tab-general'],
			'fields': ['name', 'alias', 'parent', 'container', 'short', 'description', 'published']
			}
		),
		('Изображения', {
			'classes': ['suit-tab', 'suit-tab-images'],
			'fields': ['image1', 'image2', 'image3', 'image4']
			}
		),
		('Карта', {
			'classes': ['suit-tab', 'suit-tab-map'],
			'fields': ['lat', 'lng', 'location', 'map_style']
			}
		),
		('Магазин', {
			'classes': ['suit-tab', 'suit-tab-store'],
			'fields': ['isstore', 'ecwid']
			}
		),	
		('Мета', {
			'classes': ['suit-tab', 'suit-tab-meta'],
			'fields': ['meta_key']
			}
		),		
		('Дата', {
			'classes': ['suit-tab', 'suit-tab-data'],
			'fields': ['pub_date']
			}
		),
	]
	suit_form_tabs = (('general', 'Основное'), ('images', 'Изображения'), ('map', 'Карта'), ('store', 'Магазин'), ('meta', 'Мета'), ('data', 'Дата'),)
	
	class form(forms.ModelForm): #вот этот кусок кода дополняет полее ввода картинки её превьюхой
		class Meta:
			widgets = {
				'image1': AdminImageWidget, #виджет определён в allvbg/widgets.py
				'image2': AdminImageWidget,
				'image3': AdminImageWidget,
				'image4': AdminImageWidget,
				'location':LocationWidget,
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
		('Основное', {
			'classes': ['suit-tab', 'suit-tab-general'],
			'fields': ['name', 'short', 'description']
			}
		),
		('Мета', {
			'classes': ['suit-tab', 'suit-tab-meta'],
			'fields': ['meta_key'], 'classes': ['collapse']
			}
		),		
		('Дата', {
			'classes': ['suit-tab', 'suit-tab-data'],
			'fields': ['pub_date'], 'classes': ['collapse']
			}
		),
	]
	suit_form_tabs = (('general', 'Основное'), ('meta', 'Мета'), ('data', 'Дата'),)
	class form(forms.ModelForm): #вот этот кусок кода дополняет полее ввода картинки её превьюхой
		class Meta:
			widgets = {
				'short': RedactorWidget(editor_options={'lang': 'ru'}),
				'description': RedactorWidget(editor_options={'lang': 'ru'}),
			}
	
class OrdersLisrtAdmin(admin.ModelAdmin):
	list_display = ('date', 'summ', 'user', 'lng')
	search_fields = ['user','date']
	list_filter = ['date','user']
	ordering = ('-date',)	
	
class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'short', 'start_date', 'end_date')
	search_fields = ['name']
	list_filter = ['start_date', 'end_date']
	ordering = ('-start_date',)	
	fieldsets = [
		('Основное', {
			'classes': ['suit-tab', 'suit-tab-general'],
			'fields': ['name', 'short', 'description']
			}
		),
		('Дата', {
			'classes': ['suit-tab', 'suit-tab-data'],
			'fields': ['start_date', 'end_date']
			}
		),
	]
	suit_form_tabs = (('general', 'Основное'), ('data', 'Дата'),)
	class form(forms.ModelForm): #вот этот кусок кода дополняет полее ввода картинки её превьюхой
		class Meta:
			widgets = {
				'short': RedactorWidget(editor_options={'lang': 'ru'}),
				'description': RedactorWidget(editor_options={'lang': 'ru'}),
			}
	class Media:
		js = (
			'/static/modeltranslation/js/force_jquery.js',
			'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
			'/static/modeltranslation/js/tabbed_translation_fields.js',
		)
		css = {
			'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
		}	
	
class MapAdmin(admin.ModelAdmin):
	list_display = ('title', 'value')
	search_fields = ['title']
	list_filter = ['title']
	ordering = ('-title',)	

admin.site.unregister(User)
 
class UserProfileInline(admin.StackedInline):
	model = UserProfile
	raw_id_fields = ("editor_for",)
 
class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
 
admin.site.register(User, UserProfileAdmin)	
admin.site.register(Firm, FirmAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(MapStyle, MapAdmin)
admin.site.register(OrdersLisrt, OrdersLisrtAdmin)