# # -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import ModelForm  # зависимость для переопределения полей формы в админке
from widgets import *
from models import AttachedImage
from suit.admin import SortableTabularInline


class ImageInlineForm(ModelForm):  # вот этот кусок кода дополняет полее ввода картинки её превьюхой
    class Meta:
        widgets = {
            'photo': SafeImageClearableFileInput,
        }

class ImageFirmInline(SortableTabularInline):
    form = ImageInlineForm
    model = AttachedImage
    extra = 1
    sortable = 'order'
