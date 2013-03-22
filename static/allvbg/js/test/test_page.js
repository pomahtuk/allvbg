var data_load, limiter_links;
var total_round, current_round, meta;

data_load = function(url) {
  if (url == null) {
    url = '/api/v1/firm/?container=false';
  }
  var request;
  request = $.ajax({
    url: url,
    type: "GET",
    dataType: "json"
  });
  request.done(function(result) {
    var message = JSON.stringify(result)
    var html = '';
    var data = result.objects;
    var current_page, index, object, total_pages;
    var arr, max_page, i, number_offset, paginator_html, parent, parent_text, _i, _j, _ref, _ref1, _ref2;

    for (index in data) {
      object = data[index];
      html += "<div class=\"list_element\">\n     <a href=\"" + object.id + "\"><h3>" + object.name + "</h3></a>\n  <img src=\"" + object.image1 + "\" width=\"120px\">\n \n  <div class=\"rateit\" data-pageid=\"" + object.id + "\" data-rateit-value=\"" + object.raiting + "\" data-rateit-resetable=\"false\"></div>\n <hr>\n  <p>" + object.short + "</p>\n</div>";
    }

    $('.list_wrap').html(html);

    meta = result.meta;

    total_pages = meta.total_count / meta.limit;

    total_round = Math.round(total_pages);

    if (total_pages > total_round) {
      total_round += 1;
    }

    current_page = meta.offset / meta.limit;

    current_round = Math.round(meta.offset / meta.limit);

    if (current_round > total_round - 1) {
      current_round = total_round - 1;
    }

    parent = meta.next != null ? meta.next : meta.previous != null ? meta.previous : '';
    arr = parent.split('/');
    parent_text = arr[arr.length - 1].split('&');
    if (parent_text[parent_text.length - 1].split('=')[0] === 'parent') {
      parent_text = "&" + parent_text[parent_text.length - 1];
    } else {
      parent_text = ''
    }

    number_offset = 5;

    paginator_html = '<div class="grid_12 pagination_wrap"><center><ul>';
    if (current_round <= number_offset) {
      for (i = _i = 0, _ref = current_round + number_offset; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
        if (i === current_round) {
          paginator_html += "<li><a class=\"active_page page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * i) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">" + (i + 1) + "</a></li>";
        } else {
          paginator_html += "<li><a class=\"page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * i) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">" + (i + 1) + "</a></li>";
        }
      }
    } else {
      paginator_html += "<li class=\"control page_switch\"><a class=\"page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * (current_round - 1)) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">Предыдущие</a></li>\n<li><a class=\"page_switch\" href=\"/api/v1/firm/?offset=" + 0 + "&limit=" + meta.limit + "&container=false" + parent_text + "\">1</a></li>\n<li>...</li>";
      max_page = current_round + number_offset;
      if (max_page >= total_round) {
        max_page = total_round - 1;
      }
      for (i = _j = _ref1 = current_round - number_offset; _ref1 <= max_page ? _j <= max_page : _j >= max_page; i = _ref1 <= max_page ? ++_j : --_j) {
        if (i === current_round) {
          paginator_html += "<li><a class=\"active_page page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * i) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">" + (i + 1) + "</a></li>";
        } else {
          paginator_html += "<li><a class=\"page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * i) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">" + (i + 1) + "</a></li>";
        }
      }
    }

    if (total_round - (current_round + number_offset) >= 1) {
      paginator_html += "<li>...</li>\n<li><a class=\"page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * (total_round - 1)) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">" + total_round + "</a></li>\n<li class=\"control page_switch\"><a class=\"page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * current_round) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">Следующие</a></li>";
    } else {
      if (current_round !== (total_round - 1)) {
        paginator_html += "<li class=\"control page_switch\"><a class=\"page_switch\" href=\"/api/v1/firm/?offset=" + (meta.limit * (current_round + 1)) + "&limit=" + meta.limit + "&container=false" + parent_text + "\">Следующие</a></li>";
      }
    }
    paginator_html += '</ul></center></div>';
    $(paginator_html).insertAfter('.list_wrap');

    bind_buttons();

  });
  request.fail(function(jqXHR, textStatus) {
    alert("Request failed: " + textStatus);
  });
};

var bind_buttons;

bind_buttons = function(){
  $('a.page_switch').click(function(e) {
    e.preventDefault();
    var elem, link;
    elem = $(this);
    link = elem.attr('href');
    $('.pagination_wrap').remove();
    data_load(link);
    return false;
  });
  true
};

limiter_links = function(){
  $('.limiter_wrap a').click(function(e){
    e.preventDefault();
    var elem, limit;
    elem = $(this);
    limit = elem.attr('rel');
    console.log(limit);
    return false;
  })
}

$(document).ready(function() {
   data_load();
   limiter_links();
})