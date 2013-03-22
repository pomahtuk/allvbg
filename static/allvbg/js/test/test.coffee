for index, object of data
  console.log object
  html += """<div class="list_element">
      <a href="#{object.id}"><h3>#{object.name}</h3></a>
      <img src="#{object.image1}" width="120px">
      
      <div class="rateit" data-pageid="#{object.id}" data-rateit-value="#{object.raiting}" data-rateit-resetable="false"></div>
      <hr>
      <p>#{object.short}</p>
    </div>"""
    
$('#log').html html

meta = result.meta
total_pages = meta.total_count / meta.limit
total_round = Math.round(total_pages)
total_round += 1 if total_pages > total_round
current_page = meta.offset/meta.limit
current_round = Math.round(meta.offset/meta.limit)
current_round += 1 if current_page > current_round

parent = if meta.next? 
  meta.next
else if meta.previous?
  meta.previous
else
  ''

arr = parent.split('/')
parent_text = arr[arr.length-1].split('&')
if parent_text[parent_text.length-1].split('=')[0] is 'parent'
  parent_text = "&#{parent_text[parent_text.length-1]}"

number_offset = 5

paginator_html = '<div class="grid_12 pagination_wrap"><center><ul>'

if current_round <= number_offset
  for i in [0..current_round+number_offset]
    if i is current_round
      paginator_html +=  """<li><a class="active_page page_switch" href="/api/v1/firm/?offset=#{meta.limit*i}&limit=#{meta.limit}&container=false#{parent_text}">#{i+1}</a></li>"""
    else
      paginator_html +=  """<li><a class="page_switch" href="/api/v1/firm/?offset=#{meta.limit*i}&limit=#{meta.limit}&container=false#{parent_text}">#{i+1}</a></li>"""
else
  paginator_html += """<li class="control page_switch"><a class="page_switch" href="/api/v1/firm/?offset=#{meta.limit*(current_round-1)}&limit=#{meta.limit}&container=false#{parent_text}">Предыдущие</a></li>
    <li><a class="page_switch" href="/api/v1/firm/?offset=#{0}&limit=#{meta.limit}&container=false#{parent_text}">1</a></li>
    <li>...</li>"""
  max_page = current_round + number_offset
  max_page = (total_round - 1) if max_page >= total_round
  for i in [current_round-number_offset..max_page]
    if i is current_round
      paginator_html +=  """<li><a class="active_page page_switch" href="/api/v1/firm/?offset=#{meta.limit*i}&limit=#{meta.limit}&container=false#{parent_text}">#{i+1}</a></li>"""
    else
      paginator_html +=  """<li><a class="page_switch" href="/api/v1/firm/?offset=#{meta.limit*i}&limit=#{meta.limit}&container=false#{parent_text}">#{i+1}</a></li>"""
if total_round - (current_round + number_offset) >= 1
  paginator_html += """<li>...</li>
    <li><a class="page_switch" href="/api/v1/firm/?offset=#{meta.limit*total_round-1}&limit=#{meta.limit}&container=false#{parent_text}">#{total_round}</a></li>
    <li class="control page_switch"><a class="page_switch" href="/api/v1/firm/?offset=#{meta.limit*current_round}&limit=#{meta.limit}&container=false#{parent_text}">Следующие</a></li>"""
else
  if current_round isnt total_round
    paginator_html += """<li class="control page_switch"><a class="page_switch" href="/api/v1/firm/?offset=#{meta.limit*(current_round + 1)}&limit=#{meta.limit}&container=false#{parent_text}">Следующие</a></li>"""


paginator_html += '</ul></center></div>'