from django.utils import simplejson
from tastypie import fields
from django.core.serializers import json
from tastypie.serializers import Serializer
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from allvbg.models import Firm, MapStyle

class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

class MapStyleResource(ModelResource):
    class Meta:
        queryset = MapStyle.objects.all()
        resource_name = 'map_style'
        authorization = DjangoAuthorization()
        serializer = PrettyJSONSerializer()

class FirmResource(ModelResource):
    map_style = fields.ForeignKey(MapStyleResource, 'map_style')
    parent = fields.ToOneField('self', 'parent', null=True)
    class Meta:
        queryset = Firm.objects.all()
        resource_name = 'firm'
        #excludes = ['isstore', 'ecwid', 'totalvotes', 'raiting', 'rating']
        authorization = DjangoAuthorization()
        serializer = PrettyJSONSerializer()
        filtering = {
            'container': ALL,
            'parent': ALL,
            'map_style': ALL_WITH_RELATIONS,
        }