from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django import forms
from django.db import models
from allvbgru import settings
import os
from PIL import Image

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
            file_path = '%s%s' % (settings.MEDIA_URL, file_name)
            try:            # is image
                Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
                output.append('<a target="_blank" href="%s">%s</a><br />%s <a target="_blank" href="%s">%s</a><br />%s ' % \
                    (file_path, thumbnail(file_name), _('Currently:'), file_path, file_name, _('Change:')))
            except IOError: # not image
                output.append('%s <a target="_blank" href="%s">%s</a> <br />%s ' % \
                    (_('Currently:'), file_path, file_name, _('Change:')))
            
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

              ymaps.ready(init);

              function init () {
                var tv = jQuery('#id_location');
                var ltt = jQuery('#id_lat');
                var lgg = jQuery('#id_lng');
                
                var x = ltt.val();
                var y = lgg.val();
                if(!x) x = %f;
                if(!y) y = %f;

                map = new ymaps.Map("YMapsID", {center: [y, x], zoom: 14});
                map.controls.add('zoomControl').add('typeSelector')

                myPlacemark = new ymaps.Placemark(map.getCenter(), {hintContent: ''}, {draggable: true});

                myCollection = new ymaps.GeoObjectCollection();

                myPlacemark.events.add('dragend', function (e) {
                  drag_end(e, myPlacemark);
                });

                map.geoObjects.add(myPlacemark);

                jQuery('#b1').click(function () {
                  var search_query = jQuery('#YMapsInput').val();
                  ymaps.geocode(search_query, {results: 1}).then(function (res) {

                    map.geoObjects.each(function(object){
                      map.geoObjects.remove(object);
                    })

                    res.geoObjects.each(function(object){
                      center = object.geometry.getCoordinates()
                      map.panTo(center);
                      tv.val([center[1], center[0]]);
                      ltt.val(center[1]);
                      lgg.val(center[0]);
                      geoPlacemark = new ymaps.Placemark(center, {hintContent: ''}, {draggable: true});
                      geoPlacemark.events.add('dragend', function (e) {
                        drag_end(e, geoPlacemark);
                      });
                    });

                    map.geoObjects.add(geoPlacemark);

                  });
                  return false;
                });

                var drag_end = function(e, placemark) {
                  var coordinates = placemark.geometry.getCoordinates();
                  tv.val([coordinates[1], coordinates[0]]);
                  ltt.val(coordinates[1]);
                  lgg.val(coordinates[0]);
                  e.stopPropagation();
                };

              }
            </script>	
		''' % (DEFAULT_LAT, DEFAULT_LNG))
        return mark_safe(u''.join(output))

    class Media:
        js = (
            'http://api-maps.yandex.ru/2.0/?load=package.full&lang=ru-RU',
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
