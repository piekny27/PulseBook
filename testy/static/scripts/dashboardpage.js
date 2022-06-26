$( document ).ready(function() {
    //$("#sortable").sortable();
    //$("#sortable").disableSelection();
    $('.ui-draggable').draggable({ // Make cards draggable
        stack: '#card-pile div', // Make dragged card appear above the others
        revert: false // Make dragged card return to start position
      })
         
 });