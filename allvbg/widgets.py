from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from django.db import models
from allvbgru import settings
import os
import Image

try:
    from easy_thumbnails.files import get_thumbnailer
    def thumbnail(image_path):
        thumbnailer = get_thumbnailer(image_path)
        thumbnail_options = {'crop': True, 'size': (160, 120), 'detail': True, 'upscale':True }
        t=thumbnailer.get_thumbnail(thumbnail_options)
        media_url = settings.ST_URL
        return u'<img src="%s%s" alt="%s" width="160" height="120"/>' % (media_url, t, image_path)
except ImportError:
    def thumbnail(image_path):
        absolute_url = os.path.join(settings.ST_ROOT, image_path)
        return u'<img src="%s" alt="%s" />' % (absolute_url, image_path)

class AdminImageWidget(AdminFileWidget):
    """
    A FileField Widget that displays an image instead of a file path
    if the current file is an image.
    """
    def render(self, name, value, attrs=None):
        output = []
        file_name = str(value)
        if file_name:
            file_path = '%s%s' % (settings.ST_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.ST_ROOT, file_name))
                #Image.open(file_path)
                output.append('<a target="_blank" href="%s">%s</a>' % \
                    (file_path, thumbnail(file_name),))
            except IOError: # not image
                output.append('%s <a target="_blank1" href="%s">%s</a> <br />%s ' % \
                    (_('Текущий:'), file_path, file_name, _('Изменить:')))
            
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

DEFAULT_LAT = 28.738031
DEFAULT_LNG = 60.713432

class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        output = [self.inner_widget.render(name, value, *args, **kwargs)]
        output.append(u'''
<div>
<input type="text" class="vTextField" id="YMapsInput">
<input id="b1" value="Найти!" onclick="enter();" type="button"/>
<div id="YMapsID" style="width: 620px; height: 300px;">
</div>

<script type="text/javascript">
	var map = -1
	var placemark = -1
	var tv = document.getElementById('id_location');
	var ltt = document.getElementById('id_lat');
	var lgg = document.getElementById('id_lng');
	
	window.onload = function () {
		var x = tv.value.substr(0, strpos(tv.value, ",", 0));
		var y = tv.value.substr(strpos(tv.value, ",", 0)+1, tv.value.length);
		if(!x) x = %f;if(!y) y = %f;
		map = new YMaps.Map(document.getElementById("YMapsID"));
		map.setCenter(new YMaps.GeoPoint(parseFloat(x), parseFloat(y)), 14);
		map.addControl(new YMaps.Zoom());
		placemark = new YMaps.Placemark(map.getCenter(), {draggable: true});
		map.addOverlay(placemark);
		
		YMaps.Events.observe(placemark, placemark.Events.DragEnd, function (obj) {
			tv.value = obj.getGeoPoint().getX() + ',' + obj.getGeoPoint().getY();
			ltt.value = obj.getGeoPoint().getX();
			lgg.value = obj.getGeoPoint().getY();			
		});
	};
	
	function strpos(haystack, needle, offset){
		var i = haystack.indexOf( needle, offset );
		return i >= 0 ? i : false;
	}
	
	function enter() {
		var geocoder = new YMaps.Geocoder(document.getElementById("YMapsInput").value, {results: 1});
		YMaps.Events.observe(geocoder, geocoder.Events.Load, function (geocoder) {
			placemark.setGeoPoint(this.get(0).getGeoPoint());
			map.panTo(this.get(0).getGeoPoint());
			tv.value = this.get(0).getGeoPoint().getX() + ',' + this.get(0).getGeoPoint().getY()
			ltt.value = obj.getGeoPoint().getX();
			lgg.value = obj.getGeoPoint().getY();			
		});
	}
</script>	
		''' % (DEFAULT_LAT, DEFAULT_LNG))
        return mark_safe(u''.join(output))

    class Media:
        js = (
            'http://api-maps.yandex.ru/1.1/index.xml?key=%s' % settings.YANDEX_MAP_KEY,
        )

class LocationFormField(forms.CharField):
    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value

        lat, lng = float(a), float(b)
        return "%f,%f" % (lat, lng)

class LocationField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults.update(kwargs)
        defaults['widget'] = LocationWidget
        return super(LocationField, self).formfield(**defaults)