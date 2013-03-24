from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from tinymce import models as tinymce_models
from django import forms
from djangoratings.fields import RatingField
from django.forms.widgets import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import hashlib
from datetime import *
import urllib2

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.CharField()
    message = forms.CharField(widget=Textarea())

class MapStyle(models.Model):#модель для типа маркера на карте
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
	
    def __unicode__(self): #дополнительное поле, определяет информацию. выводимю на экран
        return self.title	

class OrdersLisrt(models.Model):
	user = models.ForeignKey(User, verbose_name='Пользователь')
	summ = models.CharField(max_length=50, verbose_name='Сумма')
	date = models.DateTimeField('Дата платежа')
	lng = models.CharField(max_length=255, verbose_name='Комментарий', null=True, blank=True)	
	def __unicode__(self): #дополнительное поле, определяет информацию. выводимю на экран
		return self.lng		
		
class tst_r(models.Model):
	rating = RatingField(range=5, allow_anonymous = True, use_cookies = True)			
		
class Firm(MPTTModel):#модель БД для фирм и организаций, наследуется от класса. поддерживающего дерево
	#далее просто указываеются все необходимые поля
	#поле "имя" - не проверяется, но должно быть уникально в пределах категории.
  name = models.CharField(max_length=50, verbose_name='Название')
	#поле "псевдоним" - не проверяется, но должно быть уникально в пределах категории.
  alias = models.CharField(max_length=50, unique=True, verbose_name='Псевдоним')	
	#указание поля, благодаря которому древовидная стукрута вообще работает
  parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
	#Логическая переменная, определяющая, по сути, в каком шаблоне отображать модель
  container = models.BooleanField(verbose_name='Контейнер?', default = False)
	#короткое описание, показывается на карте и в отображении списком
  short = tinymce_models.HTMLField(verbose_name='Короткое описание', null=True, blank=True)
	#Полный текст описания фирмы
  description = tinymce_models.HTMLField(verbose_name='Полный текст', null=True, blank=True)
	#изображения, привязанные к фирме
  image1 = models.ImageField(upload_to='uploads', verbose_name='Изображение 1', null=True, blank=True)
  image2 = models.ImageField(upload_to='uploads', verbose_name='Изображение 2', null=True, blank=True)
  image3 = models.ImageField(upload_to='uploads', verbose_name='Изображение 3', null=True, blank=True)
  image4 = models.ImageField(upload_to='uploads', verbose_name='Изображение 4', null=True, blank=True)
	#ключевые слова
  meta_key = models.CharField(max_length=100, verbose_name='Ключевые слова', null=True, blank=True)
	#строка адреса фирмы
  location = models.CharField(max_length=100, verbose_name='Адрес', null=True, blank=True)
  lat = models.CharField(max_length=255, verbose_name='Широта', null=True, blank=True)
  lng = models.CharField(max_length=255, verbose_name='Долгота', null=True, blank=True)
	#стиль отображения на карте. Проще сделать отдельной таблицей все значения.
  map_style = models.ForeignKey(MapStyle, verbose_name='Стиль на карте', null=True, blank=True)
	#Логическая переменная, определяющая, является ли данный объект магазином
  isstore = models.BooleanField(verbose_name='Магазин?', default = False)
	#поле "ecwid" - необходимое поле в случае, если ресурс - магазин.
  ecwid = models.CharField(max_length=50, verbose_name='ID магазина ECWID', null=True, blank=True)
	#дата создания ресурса
  pub_date = models.DateTimeField('Дата публикации', null=True, blank=True, default = datetime.now())	
	#переменная для количества голосов
  totalvotes = models.BigIntegerField(verbose_name='Количество проголосовавших', null=True, blank=True)
	#переменная для подсчёта рейтинга
  #raiting = models.FloatField(verbose_name='Рейтинг', null=True)
  rating = RatingField(range=5, allow_anonymous = True, use_cookies = True, null=True, blank=True)
  published = models.BooleanField(verbose_name='Опубликовано?', default = False)

  class MPTTMeta:#метадата для деревьев
    order_insertion_by = ['name']
		
  def __unicode__(self): #дополнительное поле, определяет информацию. выводимю на экран
    return self.name	
		
class Event(models.Model):
	#поле "имя" - должно быть уникально.
	name = models.CharField(max_length=50, unique=True, verbose_name='Название')
	#короткое описание, показывается в отображении списком
	short = tinymce_models.HTMLField(verbose_name='Короткое описание')
	#Полный текст описания фирмы
	description = tinymce_models.HTMLField(verbose_name='Полный текст')
	#дата создания ресурса
	start_date = models.DateTimeField('Дата начала')	
	#дата создания ресурса
	end_date = models.DateTimeField('Дата окончания')
	
	def __unicode__(self): #дополнительное поле, определяет информацию. выводимю на экран
		return self.name	
		
class Article(models.Model):#модель для статьи.
	#поле "имя" - должно быть уникально.
	name = models.CharField(max_length=50, unique=True, verbose_name='Название')
	#короткое описание, показывается в отображении списком
	short = tinymce_models.HTMLField(verbose_name='Короткое описание')
	#Полный текст описания фирмы
	description = tinymce_models.HTMLField(verbose_name='Полный текст')
	#ключевые слова
	meta_key = models.CharField(max_length=100, verbose_name='Ключевые слова')
	#дата создания ресурса
	pub_date = models.DateTimeField('Дата публикации')		
	
	def __unicode__(self): #дополнительное поле, определяет информацию. выводимю на экран
		return self.name
		
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    editor_for = models.ForeignKey(Firm, verbose_name='Редактирует фирму:', null=True, blank=True)
    generated_password = models.CharField(max_length=255, verbose_name='Сгенерированный пароль', null=True, blank=True)
    generated_email = models.CharField(max_length=255, verbose_name='Сгенерированный email', null=True, blank=True)
    paid_till = models.DateTimeField('Оплачено до', null=True, blank=True)	
	
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            token = "cbe688b751993340999aceaa28432eba44eeb4eb418388e309bbdcb5"
            crc  = hashlib.md5(instance.username+str(instance.id)+"someSalT").hexdigest()[:10]
            url = "https://pddimp.yandex.ru/reg_user_token.xml?token="+token+"&u_login="+instance.username+"&u_password="+crc
            result = urllib2.urlopen(url)
            
            UserProfile.objects.create(user=instance, generated_password=crc, generated_email=instance.username+"@allvbg.ru", paid_till = datetime.now())		
			
    post_save.connect(create_user_profile, sender=User)	
	
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password','editor_for','is_staff','is_active','is_superuser','last_login','date_joined','groups','user_permissions')
			
class FirmUserForm(forms.ModelForm):
    class Meta:
        model = Firm
        exclude = ('rating','raiting','totalvotes','pub_date','ecwid','isstore','map_style','meta_key','container','alias','parent')

class FirmForm(forms.ModelForm):
  class Meta:
    model = Firm
    exclude = ('ecwid', 'isstore', 'container', 'alias', 'published')