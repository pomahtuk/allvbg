from django import forms
from geosite.models import Firm

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
