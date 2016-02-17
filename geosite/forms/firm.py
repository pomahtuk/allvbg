from django import forms
from geosite.models import Firm
from suit_redactor.widgets import RedactorWidget

class FirmUserForm(forms.ModelForm):
    class Meta:
        model = Firm
        exclude = (
            'rating',
            'raiting',
            'totalvotes',
            'pub_date',
            'ecwid',
            'isstore',
            'map_style',
            'meta_key',
            'container',
            'alias',
            'parent'
        )


class FirmForm(forms.ModelForm):
    class Meta:
        model = Firm
        exclude = ('ecwid', 'isstore', 'container', 'alias', 'published')

class FirmAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'short': RedactorWidget(editor_options={'lang': 'ru'}),
            'description': RedactorWidget(editor_options={'lang': 'ru'}),
        }
