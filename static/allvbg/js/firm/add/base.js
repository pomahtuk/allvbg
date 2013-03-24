$(document).ready(function(){

  function mapFormatResult(style) {
    if (style.value != 'none') {
      return "<img class='mapicon' src='/static/allvbg/" + style.value + "'/>" + style.title;
    } else {
      return style.title;
    }
  };

  function mapFormatSelection(style) {
      return style.title;
  };

  function parentFormatResult(firm) {
    return firm.name;
  };

  function parentFormatSelection(firm) {
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
  }

  function form_hierarchial_data(array) {
    top_level = find_in_objects_array(array, 0, 'level');
    var child_array, object, query, _i, _len;
    for (_i = 0, _len = top_level.length; _i < _len; _i++) {
      object = top_level[_i];
      query = "/api/v1/firm/" + object.id + "/";
      object.children = [];
      var deleted = delete object['id'];
      object.children = find_in_objects_array(array, query, 'parent');
    };
    return top_level;
  }


  $('#id_description').redactor();
  $('#id_short').redactor();

  $.ajax({
    url: "http://allvbg.ru/api/v1/firm/?limit=120&container=true",
    dataType: 'jsonp',
  }).done(function(data) {
    var results = form_hierarchial_data(data.objects);
    $('#id_parent').select2({
      data:{ results: results, text: 'name' },
      formatResult: parentFormatResult, 
      formatSelection: parentFormatSelection
    });
  })

  $.ajax({
    url: "http://allvbg.ru/api/v1/map_style/?limit=120",
    dataType: 'jsonp',
  }).done(function(data) {
    $('#id_map_style').select2({
      data:{ results: data.objects, text: 'title' },
      formatResult: mapFormatResult, 
      formatSelection: mapFormatSelection,
      escapeMarkup: function (m) { return m; }
    });
  });

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

  }
  
});