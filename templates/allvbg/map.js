{% load thumbnail %}
        // Создание обработчика для события window.onLoad
        YMaps.load(function () {
            // Создание экземпляра карты и его привязка к созданному контейнеру
            var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);

            // Установка для карты ее центра и масштаба
            map.setCenter(new YMaps.GeoPoint(28.762311,60.705288), 14);

            // Добавление элементов управления
            map.addControl(new YMaps.ToolBar());
            map.addControl(new YMaps.Zoom());
			map.disableScrollZoom();
			map.addControl(new YMaps.SearchControl());

	  
	    			//стили
			var baseStyle = new YMaps.Style();
			baseStyle.iconStyle = new YMaps.IconStyle();
			baseStyle.iconStyle.offset = new YMaps.Point(-12, -28);
			baseStyle.iconStyle.size = new YMaps.Point(24, 28);
			
				{% if styles %}
					{% for style in styles %}
						var {{ style.title }} = new YMaps.Style(baseStyle);
						{{ style.title }}.iconStyle = new YMaps.IconStyle();
						{{ style.title }}.iconStyle.href = "{{ STATIC_URL }}allvbg/{{ style.value }}";
					{% endfor %}
				{% endif %}
				
			var groups = [
				{% block groups %}
				//сюда, сюда! Все сюда!
				{% load mptt_tags %}
					{% full_tree_for_model allvbg.firm as firms %}
									
					{% recursetree firms %}
						{% if node.level == 0 or node.level == 1 %} createGroup("{{ node.name }}", [ {% endif %}
						{% if node.level == 2 %} createPlacemark(new YMaps.GeoPoint({{ node.location }}), '<center style=\"padding-bottom:5px;\">{{ node.name|safe }}</center>','<img src=\"{{ STATIC_URL }}allvbg/{{ node.image1 }}\" align=\"left\" width=\"80\" height=\"80\" alt=\"{{ node.name|safe }}\"><div style=\"width:150px; margin-left:85px;\">{{ node.short|safe }}<br><a class="pdr" href=\"{{ node.id }}">Подробнее...</a></div>', {style: {{ node.map_style }} }), {% endif %}
							{% if not node.is_leaf_node %}
									{{ children }}
							{% endif %}
						{% if node.level == 0 or node.level == 1 %} ]), {% endif %}
					{% endrecursetree %}
				{% endblock %}
			]
			
			
			{% block logic %}
           for (var i = 0; i < groups.length; i++) {
				addMenuItem(groups[i], map, YMaps.jQuery("#menu"),i);			
				for (var j=0; j<groups[i]._objects.length; j++){
					addMenuSubItem(groups[i]._objects[j], map, YMaps.jQuery("#menu"+i));
				  map.addOverlay(groups[i]._objects[j]);
				}
				//map.addOverlay(groups[i]);
            }
        })

        // Добавление одного пункта в список
        function addMenuItem (group, map, menuContainer,i) {

            // Показать/скрыть группу на карте
	  YMaps.jQuery("<a class=\"title active\" href=\"#\">" + group.title + "</a><img src=\"{{ STATIC_URL }}allvbg/img/sld.png\" width=\"16px\" height=\"16px\" alt=\" \" style=\"margin-left:5px; position:relative; top:4px;\" >")
                .bind("click", function () {
					
		    $("#menu"+i).slideToggle("slow");
					

                    return false;
                })

                // Добавление нового пункта меню в список
                .appendTo(
                    YMaps.jQuery("<li></li>").appendTo(menuContainer)
                )
			
			YMaps.jQuery("<div id=\"menu"+i+"\"></div>").appendTo(menuContainer);
			
        };
		
        function addMenuSubItem (group, map, menuContainer) {

            // Показать/скрыть группу на карте
	  if (group._objects[0]===undefined){
            YMaps.jQuery("<img src=\"{{ STATIC_URL }}allvbg/img/transparent.png\" width=\"24\" height=\"27\" align=\"left\" style=\"margin-right:5px;\" alt=\" \" /><a class=\"title_sub active_sub\" href=\"#\">" + group.title + "</a>")
                .bind("click", function () {
							
                    var link = YMaps.jQuery(this);

                    // Если пункт меню "неактивный", то добавляем группу на карту,
                    // иначе - удаляем с карты
                    if (link.hasClass("active_sub")) {
                        map.removeOverlay(group);
                    } else {
                        map.addOverlay(group);
                    }

                    // Меняем "активность" пункта меню
                    link.toggleClass("active_sub");

                    return false;
                })

                // Добавление нового пункта меню в список
                .appendTo(
                    YMaps.jQuery("<li></li>").appendTo(menuContainer)
                )
	      } else{
            	YMaps.jQuery("<img src=\""+group._objects[0]._computedStyle.iconStyle.href+"\" width=\"24\" height=\"27\" align=\"left\" style=\"margin-right:5px;\" alt=\" \" /><a class=\"title_sub active_sub\" href=\"#\">" + group.title + "</a>")
                .bind("click", function () {
							
                    var link = YMaps.jQuery(this);

                    // Если пункт меню "неактивный", то добавляем группу на карту,
                    // иначе - удаляем с карты
                    if (link.hasClass("active_sub")) {
                        map.removeOverlay(group);
                    } else {
                        map.addOverlay(group);
                    }

                    // Меняем "активность" пункта меню
                    link.toggleClass("active_sub");

                    return false;
                })

                // Добавление нового пункта меню в список
                .appendTo(
                    YMaps.jQuery("<li></li>").appendTo(menuContainer)
                )			
	      }
        };		
		


        // Создание группы
        function createGroup (title, objects, style) {
            var group = new YMaps.GeoObjectCollection(style);

            group.title = title;
            group.add(objects);
            
            return group;
        };

        // Создание метки
        function createPlacemark (point, name, description, style) {
            var placemark = new YMaps.Placemark(point, style);

            placemark.name = name;
            placemark.description = description;

            return placemark
        }
		{% endblock %}