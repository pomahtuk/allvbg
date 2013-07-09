$(document).ready(function(){

  function mapCategoryFormat(object) {
    if (object.level === 0) {
      return object.name;
    } else{ 
      if ((object.style_img != 'none') & (object.style_img != 'undefined')) {
        return "<img class='mapicon' src='/static/allvbg/" + object.style_img + "'/>" + object.name;
      } else {
        return object.name;
      }
    }
  };

  function mapCategorySelection(firm) {
    return firm.name;
  };

  function find_in_objects_array(array, query, field) {
    var result = [];
    for (_i = 0, _len = array.length; _i < _len; _i++) {
      item = array[_i];
      if (item[field] == query) {
        result.push(item);
      }
    }
    return result
  };

  function form_hierarchial_data(firms, styles) {
    top_level = find_in_objects_array(firms, 0, 'level');
    var child_array, object, query, _i, _len;
    for (_i = 0, _len = top_level.length; _i < _len; _i++) {
      object           = top_level[_i];

      query            = "/api/v1/firm/" + object.id + "/";
      object.children  = [];
      var deleted      = delete object['id'];
      object.children  = find_in_objects_array(firms, query, 'parent');

      var children, _j, _j_len;
      for (_j = 0, _j_len = object.children.length; _j < _j_len; _j++) {
        children = object.children[_j];
        style_id         = children.map_style.split('/map_style/')[1].split('/')[0];
        style_img        = find_in_objects_array(styles, style_id, 'id')[0];
        children.style_img = style_img.value;
      }

    };

    return top_level;
  };

  function ajax_get(url, callback) {
    $.ajax({
      url: url,
      dataType: 'jsonp',
    }).done(function(data) {
      if (callback) callback(data.objects);
    });
  };

  flow_test = function() {
    flow.exec(
      function() {
        ajax_get("http://allvbg.ru/api/v1/firm/?limit=120&container=true", this.MULTI('firm'));
        ajax_get("http://allvbg.ru/api/v1/map_style/?limit=120", this.MULTI('style'));
      },function(results) {
        new_results = form_hierarchial_data(results['firm'], results['style']); 
        $('#id_parent').select2({
          data:{ results: new_results, text: 'name' },
          formatResult: mapCategoryFormat, 
          formatSelection: mapCategorySelection
        });
      }
    );
  };

  $('#id_description').redactor();
  $('#id_short').redactor();
  flow_test();

  ymaps.ready(init);

  function init () {
    var tv = $('#id_location');
    var ltt = $('#id_lat');
    var lgg = $('#id_lng');
    
    var x = ltt.val();
    var y = lgg.val();
    if(!x) x = 28.738031;
    if(!y) y = 60.713432;

    map = new ymaps.Map("YMapsID", {center: [y, x], zoom: 14});
    map.controls.add('zoomControl').add('typeSelector')

    myPlacemark = new ymaps.Placemark(map.getCenter(), {hintContent: ''}, {draggable: true});

    myCollection = new ymaps.GeoObjectCollection();

    myPlacemark.events.add('dragend', function (e) {
      drag_end(e, myPlacemark);
    });

    map.geoObjects.add(myPlacemark);

    $('#b1').click(function () {
      var search_query = $('#YMapsInput').val();
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

  };
  
});