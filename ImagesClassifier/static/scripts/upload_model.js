$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  var count = 0; 
  
  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',

    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
			$("#gallery").prepend("<a onclick='load_data(" + "\" " + data.result.url + "\" " + ")' >" + data.result.name + "</a><br>")
      }
    }
  });

});