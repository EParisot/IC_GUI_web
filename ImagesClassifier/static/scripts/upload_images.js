$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });
  
  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
	/* PROGRESSBAR */
    start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
      $("#modal-progress").modal("show");
    },
    stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
      $("#modal-progress").modal("hide");
    },
    progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
		var a = document.createElement('a');
		a.setAttribute("onclick", "show_pic('" + data.result.url + "', '" + data.result.name + "')");
		
		var img = document.createElement('IMG');
		img.src = data.result.url;
		img.alt = data.result.name;
		img.width = 160;
		img.height = 120;
		
		a.appendChild(img);

		a.style.margin = "5px 5px 5px 5px";
		a.selected = false;
		a.addEventListener('click', function(event)
								{
											if (a.selected==false)
											{
												var img_list = document.getElementById('gallery').querySelectorAll('a'), i;
												for (i = 0; i < img_list.length; ++i)
												{
													img_list[i].style.outline="";
													img_list[i].selected = false;
												}
												a.style.outline="4px solid red";
												a.selected=true;
											}
											else
											{
												a.style.outline="";
												a.selected=false;
											}
											
											show_pic(data.result.url, data.result.name);
								}
							)
		
		
		var pic_div = document.getElementById("gallery");
		pic_div.appendChild(a);
		pic_div.scrollTop = pic_div.scrollHeight;
		
		var img_list = document.getElementById('gallery').querySelectorAll('a');
		var count_h1 = document.getElementById("count_h1");
		count_h1.innerHTML = img_list.length.toString() + " pics";
      }
    }
  });

});