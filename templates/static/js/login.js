$(() => {

    $("input").on("focus", function(event) {
      const div = $(this).parent(".input-field");
      const label = div.children("label");
      
      label.css("top", "-10px");
    });
    
    $("input").on("blur", function(event) {
      const div = $(this).parent(".input-field");
      const label = div.children("label");
      
      if ($(this).val().length == 0) {
        label.css("top", "12px");
      }
    });
  
  });