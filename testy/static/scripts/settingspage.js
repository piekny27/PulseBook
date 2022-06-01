$(document).ready(function() {
  
    console.log("ready!");
    var $total = 4;
    var $width = 100/$total;
    $(document).find('li.aaa').css('width',$width-1 + '%');
    
    var $current = 0;
    var $prev = undefined;
  
    updateProgress();
  
    function updateProgress()
    {
      var move_distance = 100 / $total;
      move_distance = move_distance * ($current) + move_distance / 2;
      $(document).find($('.progress-bar')).css({width: move_distance + '%'});
      changeTab();
      
      var $item1 = $(document).find('.circle-border').eq($prev);
      var $item2 = $(document).find('.circle-border').eq($current);
      var $item3 = $(document).find('.circle-fill').eq($current);
      var $item4 = $(document).find('.circle-fill').eq($prev);
      var $item5 = $(document).find('.fa-solid').eq($current);
      var $item6 = $(document).find('.fa-solid').eq($prev);
      
      //border
      $item1.addClass('checked');
      
      //fill
      $item3.removeClass('anim-fill-out');
      $item4.removeClass('anim-fill-in');
      $item3.addClass('anim-fill-in');
      $item4.addClass('anim-fill-out');
      
      //icon
      $item5.removeClass('anim-icon-out');
      $item6.removeClass('anim-icon-in');
      $item5.addClass('anim-icon-in');
      $item6.addClass('anim-icon-out');
    }
  
    function next()
    {
      if($current >=0 && $current<$total-1)
      {
        $prev=$current;
        $current++;
      }
      updateProgress();
      console.log($current);
    }
    function prev()
    {
     if($current >0 && $current<$total)
      {
        $prev=$current;
        $current--;
      }
      updateProgress();
      console.log($current);
    }
    
    function toggle()
    {
      var selector = $('ul').find('.circle-validate').eq($current)
      if(selector.hasClass('anim'))
      {
        selector.removeClass('anim');
        console.log('remove');
      }
      else
      {
        selector.addClass('anim');
        console.log('add');
      }
    }
    
    function change(event)
    {
      if(event.data.id != $current)
      {
        $prev=$current;
        $current = event.data.id;
        updateProgress();
        console.log(event.data.id);
      } 
    }
    
    function changeTab()
    {
      $(document).find('#menu'+$prev).removeClass('active');
      $(document).find('#menu'+$current).addClass('active');
    }
  
    $('button.prev').on('click', prev);
    $('button.next').on('click', next);
    $('button.toggle').on('click', toggle);
    $('#tab1').on("click", {id: "0"}, change);
    $('#tab2').on("click", {id: "1"}, change);
    $('#tab3').on("click", {id: "2"}, change);
    $('#tab4').on("click", {id: "3"}, change);
    
  });
  
  