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
  
  $('#slider1').anythingSlider({
    easing          : 'linear',
    buildArrows     : false,
    buildNavigation : false,
    animationTime   : 500
  });
  
  $(".xtrig").click(function(){
    $('.xtrig').removeClass('activetab');
    $('#slider1').anythingSlider($(this).data('rel'));
    $(this).addClass('activetab');
    return false;
  });

  $('.langpair').click(function(){
    var elem = $(this);
    $('#language').val(elem.data('value'));
    $('#langform').submit();
  });

  $(".ajax.add_firm").fancybox({
      openEffect  : 'none',
      closeEffect : 'none',
      width       : 960
  });

  $("#fast-feedback-btn").fancybox({
      openEffect  : 'none',
      closeEffect : 'none',
      width       : 600,
      height      : 450,
      scrolling   : 'no'
  });

});  