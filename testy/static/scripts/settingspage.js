
window.onload = function () {
  console.log(config_state);
};

$(document).ready(function () {

  console.log("ready!");
  var $total = 4;
  var $width = 100 / $total;
  $(document).find('li.aaa').css('width', $width - 1 + '%');


  var $current = 0;
  if(config_state == 0)
  {
    $current = 0;
  }
  if(config_state == 1)
  {
    $current = 2;
  }
  if(config_state == 2)
  {
    $current = 3;
  }
  var $prev = undefined;

  updateProgress();

  function updateProgress() {
    var move_distance = 100 / $total;
    move_distance = move_distance * ($current) + move_distance / 2;
    $(document).find($('.progress-bar')).css({ width: move_distance + '%' });
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

    //device update
    switch ($current) {
      case '0':
        console.log('Menu0');
        $("#preev").hide();
        break;
      case '1':
        $("#preev").show();
        console.log('Menu1');
        break;
      case '2':
        $("#preev").show();
        console.log('Menu2');
        break;
      case '3':
        $("#preev").show();
        console.log('Menu3');
        break;
    }


  }



  function next() {
    if ($current >= 0 && $current < $total - 1) {
      $prev = $current;
      $current++;
    }
    updateProgress();
    console.log($current);
  }
  function prev() {
    if ($current > 0 && $current < $total) {
      $prev = $current;
      $current--;
    }
    updateProgress();
    console.log($current);
  }

  function toggle() {
    var selector = $('ul').find('.circle-validate').eq($current)
    if (selector.hasClass('anim')) {
      selector.removeClass('anim');
      console.log('remove');
    }
    else {
      selector.addClass('anim');
      console.log('add');
    }
  }

  function change(event) 
  {
    var curr = event.data.id;
    if(config_state == 0 && (curr == 0 || curr == 1) ||
       config_state == 1 && (curr == 2) ||
       config_state == 2 && (curr == 3)
       )
    {
      if(event.data.id != $current) 
      {
        $prev = $current;
        $current = event.data.id;
        updateProgress();
        
      }
    }
  }
  function change2(page) 
  {
    if(config_state == 0 && (page == 0 || page == 1) ||
       config_state == 1 && (page == 2) ||
       config_state == 2 && (page == 3)
       )
    {
      if(page != $current) 
      {
        $prev = $current;
        $current = page
        updateProgress();
      }
    }
  }

  function changeTab() {
    $(document).find('#menu' + $prev).removeClass('active');
    $(document).find('#menu' + $current).addClass('active');
  }


  $("#dk").click(function () {
    if($current == 1)
    {
      $("#dk").css("border", "1px solid black");
    }
  });

  $("#device_ok").click(function () {
    var text = $("#dk").val();
    if (text) {
      toggle()
      $.ajax({
        url: "/settings",
        type: "get",
        data: { device_key: text },
        success: function (response) {
          $("#dk").prop("readonly", true);
          toggle();
          config_state++;
          $current++;
          change2($current);
          location.reload()
        },
        error: function (xhr) {
          console.log('background red');
          $("#dk").css("border", "1px solid red");
          toggle();
        }
      });
    }

  });

  $("#pin_ok").click(function () {
    var text = $("#pin").val();
    if (text) {
      toggle()
      $.ajax({
        url: "/settings",
        type: "get",
        data: { pin: text },
        success: function (response) {
          $("#pin").prop("readonly", true);
          $('#pin').css('cursor', 'default');
          toggle();
          config_state++;
          $current++;
          change2($current);
          location.reload()
        },
        error: function (xhr) {
          console.log('background red');
          $("#pin").css("border", "1px solid red");
          toggle();
        }
      });
    }
  });

  $("#delete_device").click(function () {
      $.ajax({
        url: "/settings",
        type: "get",
        data: { delete_device: true },
        success: function (response) {
          console.log('refresh');
          location.reload()
        },
        error: function (xhr) {
          console.log('background red');
          $("#pin").css("border", "1px solid red");
          toggle()
        }
      });
  });


  $('button.prev').on('click', prev);
  $('button.next').on('click', next);
  //$('button.toggle').on('click', toggle);
  $('#tab1').on("click", { id: "0" }, change);
  $('#tab2').on("click", { id: "1" }, change);
  $('#tab3').on("click", { id: "2" }, change);
  $('#tab4').on("click", { id: "3" }, change);

});

