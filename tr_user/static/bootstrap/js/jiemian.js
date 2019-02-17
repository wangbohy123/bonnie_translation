$('.u2 li').mouseenter(function(){
      $(this).css({'background':'gray'});
      $(this).find('span').css({'color':'gold'});
      $('.u2 li').not($(this)).css({'background':'#339966'});
      $(this). find('.right').show();
      $('.right').not($(this).find('.right')).hide();
});
$('.u2 li').mouseleave(function(){
      $(this).find('.right').hide();
      $(this).find('span').css({'color':'gold'});
      $(this).css({'background':'#339966'});
});
