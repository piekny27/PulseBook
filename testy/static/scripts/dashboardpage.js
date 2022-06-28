$( document ).ready(function() {
    //$("#sortable").sortable();
    //$("#sortable").disableSelection();
    $('.ui-draggable').draggable({ // Make cards draggable
        stack: '.card', // Make dragged card appear above the others
        revert: false, // Make dragged card return to start position
        handle: ".card-header",
        containment: ".card-block",
        snap:[10,10]
      })
 });