from django.template import Library, TemplateSyntaxError
import os
from PIL import Image
from datetime import date, timedelta, time
from allvbg.models import Event, Firm, Article
import urllib, feedparser
from django import template
import time
from django.template.defaultfilters import stringfilter
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from djangoratings.models import Vote

register = Library()

@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  
  if value!=None:  
    return range(1, value+1 )
  
@register.filter
def pagination(firms, adjacent_pages=5):
    page_list = range(max(1,firms.number - adjacent_pages), min(firms.paginator.num_pages,firms.number + adjacent_pages) + 1)
    if not 1 in page_list:
        page_list.insert(0,1)
        if not 2 in page_list:
            page_list.insert(1,'.')
    if not firms.paginator.num_pages in page_list:
        if not firms.paginator.num_pages - 1 in page_list:
            page_list.append('.')
        page_list.append(firms.paginator.num_pages)
    return page_list
  
THUMBNAILS = 'thumbnails'
SCALE_WIDTH = 'w'
SCALE_HEIGHT = 'h'

def scale(max_x, pair):
    x, y = pair
    new_y = (float(max_x) / x) * y
    return (int(max_x), int(new_y))
    
# Thumbnail filter based on code from http://batiste.dosimple.ch/blog/2007-05-13-1/
@register.filter
def thumbnail(original_image_path, arg):  
    if not original_image_path:  
        return ''  
        
    if arg.find(','):
        size, upload_path = [a.strip() for a in  arg.split(',')]
    else:
        size = arg
        upload_path = ''
		
	#if upload_path == 'default':
	#	upload_path = ST_PATH

    if (size.lower().endswith('h')):
        mode = 'h'
    else:
        mode = 'w'
        
    # defining the size  
    size = size[:-1]
    max_size = int(size.strip())
    
    # defining the filename and the miniature filename  
    basename, format = original_image_path.rsplit('.', 1)  
    basename, name = basename.rsplit(os.path.sep, 1)  

    miniature = name + '_' + str(max_size) + mode + '.' + format
    thumbnail_path = os.path.join(basename, THUMBNAILS)
    if not os.path.exists(thumbnail_path):  
        os.mkdir(thumbnail_path)  
    
    miniature_filename = os.path.join(thumbnail_path, miniature)  
    miniature_url = '/'.join((settings.MEDIA_URL, upload_path, THUMBNAILS, miniature))  
    
    # if the image wasn't already resized, resize it  
    if not os.path.exists(miniature_filename) \
        or os.path.getmtime(original_image_path) > os.path.getmtime(miniature_filename):
        image = Image.open(original_image_path)  
        image_x, image_y = image.size  
        
        if mode == SCALE_HEIGHT:
            image_y, image_x = scale(max_size, (image_y, image_x))
        else:
            image_x, image_y = scale(max_size, (image_x, image_y))
            
        
        image = image.resize((image_x, image_y), Image.ANTIALIAS)
              
        image.save(miniature_filename, image.format)  

    return miniature_url
	
def get_last_day_of_month(year, month):
    if (month == 12):
        year += 1
        month = 1
    else:
        month += 1
    return date(year, month, 1) - timedelta(1)

@register.inclusion_tag('agenda/month_cal.html')
def month_cal(year=date.today().year, month=date.today().month):

    first_day_of_month = date(year, month, 1)
    last_day_of_month = get_last_day_of_month(year, month)
    first_day_of_calendar = first_day_of_month - timedelta(first_day_of_month.weekday())
    last_day_of_calendar = last_day_of_month + timedelta(7 - last_day_of_month.weekday())
	
    event_list = Event.objects.filter(end_date__gte=first_day_of_calendar, start_date__lte=last_day_of_calendar)	
	
    month_cal = []
    week = []
    week_headers = []
    extra = {}
	
    if first_day_of_month.month==12:
        tmp_y = first_day_of_month.year+1
        extra['next_date'] = str(tmp_y)+',1'
    else:
        tmp_m = first_day_of_month.month+1
        extra['next_date'] = str(first_day_of_month.year)+','+str(tmp_m)		

    if first_day_of_month.month==1:
        tmp_y = first_day_of_month.year-1
        extra['prev_date'] = str(tmp_y)+',12'
    else:
        tmp_m = first_day_of_month.month-1
        extra['prev_date'] = str(first_day_of_month.year)+','+str(tmp_m)		
	
    extra['date'] = first_day_of_month
	
    i = 0
    day = first_day_of_calendar
    while day <= last_day_of_calendar:
        if i < 7:
            week_headers.append(day)
        cal_day = {}
        cal_day['day'] = day
        cal_day['isevent'] = False
        for event in event_list:
            if day >= event.start_date.date() and day <= event.end_date.date():
                cal_day['isevent'] = True
                cal_day['events'] = event_list.filter(end_date__gte=event.start_date.date, start_date__lte=event.end_date.date)
        if day.month == month:
            cal_day['in_month'] = True
        else:
            cal_day['in_month'] = False 
        if day.weekday() == 5 or day.weekday() == 6:
            cal_day['weekend'] = True			
        week.append(cal_day)
        if day.weekday() == 6:
            month_cal.append(week)
            week = []
        i += 1
        day += timedelta(1)

    return {'calendar': month_cal, 'headers': week_headers, 'extra':extra}

@register.filter
def rupluralize(value, endings):
    try:
        endings = endings.split(',')
        if value % 100 in (11, 12, 13, 14):
            return endings[2]
        if value % 10 == 1:
            return endings[0]
        if value % 10 in (2, 3, 4):
            return endings[1]
        else:
            return endings[2]
    except:
        raise TemplateSyntaxError
  
@register.filter
def getlink(value):
	item = Firm.objects.get(pk=value)
	if item.level == 0:
		return item.alias
	elif item.level == 1:
		return item.parent.alias+'/'+item.alias
	else:
		return item.parent.parent.alias+'/'+item.parent.alias+'/'+item.alias+'.html'
  
class RatingByRequestNode(template.Node):
    def __init__(self, request, obj, context_var):
        self.request = request
        self.obj, self.field_name = obj.split('.')
        self.context_var = context_var
    
    def render(self, context):
        try:
            request = template.resolve_variable(self.request, context)
            obj = template.resolve_variable(self.obj, context)
            field = getattr(obj, self.field_name)
        except (template.VariableDoesNotExist, AttributeError):
            return ''
        try:
            vote = field.get_rating()
            context[self.context_var] = str(vote)
        except ObjectDoesNotExist:
            context[self.context_var] = 0
        return ''
		
def do_rating_by_object(parser, token):
    """
    Retrieves the ``Vote`` cast by all users on a particular object and
    stores it in a context variable. If the users has not voted, the
    context variable will be 0.
    
    Example usage::
    
        {% rating_by_object request on instance as vote %}
    """
    
    bits = token.contents.split()
    if len(bits) != 6:
        raise template.TemplateSyntaxError("'%s' tag takes exactly five arguments" % bits[0])
    if bits[2] != 'on':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'on'" % bits[0])
    if bits[4] != 'as':
        raise template.TemplateSyntaxError("fourth argument to '%s' tag must be 'as'" % bits[0])
    return RatingByRequestNode(bits[1], bits[3], bits[5])
register.tag('do_rating_by_object', do_rating_by_object)

@register.inclusion_tag('agenda/message.html')
def get_hello(key = 2):
	article = Article.objects.get(pk=key)
	return {'article': article}

import urllib, os, time, datetime, feedparser
CACHE_FOLDER = '/var/www/pman/data/www/allvbgru/rss_cache/'

@register.inclusion_tag('agenda/rss_block.html')
def pull_feed(feed_url, posts_to_show=3, cache_expires=30):
    CACHE_FILE = ''.join([CACHE_FOLDER, template.defaultfilters.slugify(feed_url), '.cache'])
    try:
        cache_age = os.stat(CACHE_FILE)[8]
    except: #if file doesn't exist, make sure it gets created
        cache_age = 0
    #is cache expired? default 30 minutes (30*60)
    if (cache_age + cache_expires*60 < time.time()):
        try: #refresh cache
            urllib.urlretrieve(feed_url,CACHE_FILE)
        except IOError: #if downloading fails, proceed using cached file
            pass
    #load feed from cache
    feed = feedparser.parse(open(CACHE_FILE))
    posts = []
    for i in range(posts_to_show):
        pub_date = feed['entries'][i].updated_parsed
        published = datetime.date(pub_date[0], pub_date[1], pub_date[2] )
        posts.append({
            'title': feed['entries'][i].title,
            'summary': feed['entries'][i].summary,
            'link': feed['entries'][i].link,
            'date': published,
        })
    return {'posts': posts}