{% extends 'allvbg/map.js' %}

{% block groups %}

{% load mptt_tags %}

{% drilldown_tree_for_node page as drilldown %}

{% for node in drilldown %}
	{% if node.level > page.level %}
		{% if node.level = 1 %}
			createGroup("{{ node.name }}", [
			{% drilldown_tree_for_node node as nodedrill %}
			{% for node in nodedrill %}
				{% if node.level > 1 %}
					createPlacemark(new YMaps.GeoPoint({{ node.location }}), '<center style=\"padding-bottom:5px;\">{{ node.name|safe }}</center>','<img src=\"{{ STATIC_URL }}allvbg/{{ node.image1 }}\" align=\"left\" width=\"80\" height=\"80\" alt=\"{{ node.name|safe }}\"><div style=\"width:150px; margin-left:85px;\">{{ node.short|safe }}<br><a class="pdr" href=\"{{ node.id }}">Подробнее...</a></div>', {style: {{ node.map_style }} }),
				{% endif %}
			{% endfor %}
			]),
		{% else %}
			createGroup("{{ node.name }}", [createPlacemark(new YMaps.GeoPoint({{ node.location }}), '<center style=\"padding-bottom:5px;\">{{ node.name|safe }}</center>','<img src=\"{{ STATIC_URL }}allvbg/{{ node.image1 }}\" align=\"left\" width=\"80\" height=\"80\" alt=\"{{ node.name|safe }}\"><div style=\"width:150px; margin-left:85px;\">{{ node.short|safe }}<br><a class="pdr" href=\"{{ node.id }}">Подробнее...</a></div>', {style: {{ node.map_style }} })]),
		{% endif %}
	{% endif %}
{% endfor %}

{% endblock %}


{% block logic %}

	for (var i = 0; i < groups.length; i++) {
		addMenuItem(groups[i], map, YMaps.jQuery("#menu"));
		map.addOverlay(groups[i]);
		}
	})

	function addMenuItem(group, map, menuContainer) {
		if (group._objects[0] === undefined) {
			YMaps.jQuery("<a class=\"title active_sub\" href=\"#\">" + group.title + "</a>").bind("click", function () {
				var link = YMaps.jQuery(this);
				if (link.hasClass("active_sub")) {
					map.removeOverlay(group);
				} else {
					map.addOverlay(group);
				}
				link.toggleClass("active_sub");
				return false;
			}).appendTo(YMaps.jQuery("<li></li>").appendTo(menuContainer))
		} else {
			YMaps.jQuery("<img src=\"" + group._objects[0]._computedStyle.iconStyle.href + "\" width=\"24\" height=\"27\" align=\"left\" style=\"margin-right:5px;\" alt=\" \" /><a class=\"title active_sub\" href=\"#\">" + group.title + "</a>").bind("click", function () {
				var link = YMaps.jQuery(this);
				if (link.hasClass("active_sub")) {
					map.removeOverlay(group);
				} else {
					map.addOverlay(group);
				}
				link.toggleClass("active_sub");
				return false;
			}).appendTo(YMaps.jQuery("<li></li>").appendTo(menuContainer))
		}
	};

	function createGroup(title, objects, style) {
		var group = new YMaps.GeoObjectCollection(style);
		group.title = title;
		group.add(objects);
		return group;
	};

	function createPlacemark(point, name, description, style) {
		var placemark = new YMaps.Placemark(point, style);
		placemark.name = name;
		placemark.description = description;
		return placemark
	}
	
{% endblock %}