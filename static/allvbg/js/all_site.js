$(document).ready(function() {  

  $('.parent > a').mouseenter(function() {
    var menu=$('.dropped_menu');
    $('.parent > a').removeClass('active_menu');
    menu.remove();
    $('body').append('<div class="dropped_menu rounder_transpoarent">'+$(this).next().html()+'</div>');
    menu=$('.dropped_menu');
    menu.append('<div class="clear"></div>');
    var position=$(this).offset();
    menu.offset({left:position.left, top:position.top+35});
    menu.animate({ opacity: "show" }, "500");
    $('.antimouse').show();       
    $('.antimouse').mouseenter(function() {
      menu.animate({ opacity: "hide" }, "500");
      menu.remove();
      $('.antimouse').hide();
      $('.parent > a').removeClass('active_menu');          
    });
    $(this).addClass('active_menu');
  });
  
  $('.deleter').click(function(){
    $('#fast-feedback-btn').hide();
  })

  $('#fast-feedback-btn').click(function(){
    var contact_form =   '<div id="contact_form">';
      contact_form   +=  '    <iframe src="/contact/" width="600" height="450"  scrolling="no" allowtransparency>Ваш браузер не поддерживает плавающие фреймы!</iframe>' ;
      contact_form   +=  '</div>';
    $('body').prepend(contact_form);
  })

  $('#slider1').anythingSlider({
    easing          : 'linear',
    buildArrows     : false,
    buildNavigation : false,
    animationTime   : 500
  });
  
  $(".xtrig").click(function(){
    $('.xtrig').removeClass('activetab');
    $('#slider1').anythingSlider($(this).attr('rel'));
    $(this).addClass('activetab');
    return false;
  });

});  