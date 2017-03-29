$(document).ready(function() {

  // Click: toggle the pull button
  $(document).on('click', '#pull', function() {
    $('ul.xs-show').slideToggle();
  });
  
  // Click: toggle the sx-show menus
  $(document).on('click', 'ul.click li.hasSubMenu', function() {
    $this = $(this);
    $subUl = $this.children().first().next();    // Submenu
    if (!$subUl.is(':visible')) {  // If submenu is hidden, toggle the submenu; otherwise issue a request
      $subUl.slideToggle();
      return false;
    }
  });
    
});

