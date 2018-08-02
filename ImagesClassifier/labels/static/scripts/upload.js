$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  var count = 0; 
  
  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
	/* PROGRESSBAR */
	//sequentialUploads: true,  /* 1. SEND THE FILES ONE BY ONE */
    //start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
    //  $("#modal-progress").modal("show");
    //},
    //stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
    //  $("#modal-progress").modal("hide");
    //},
    //progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
    //  var progress = parseInt(data.loaded / data.total * 100, 10);
    //  var strProgress = progress + "%";
    //  $(".progress-bar").css({"width": strProgress});
    //  $(".progress-bar").text(strProgress);
    //},
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
		var a = document.createElement('a');
		count += 1;
		a.id = "x" + count.toString();
		a.src = data.result.url;
		
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
												a.style.outline="4px solid black";
												a.selected=true;
											}
											else
											{
												a.style.outline="";
												a.selected=false;
											}
											
											show_pic(data.result.url);
											var p = document.getElementById('pic_p')
											p.innerHTML = data.result.name;
								}
							)
		
		
		var pic_div = document.getElementById("gallery");
		pic_div.appendChild(a);
		pic_div.scrollTop = pic_div.scrollHeight;
      }
    }
  });

});

(function show_pic(url)
{
	var img = document.createElement("IMG");
	img.src = url;
	img.height = 120;
	img.width = 160;
	if (document.getElementById('pic_div').childElementCount!=0)
	{
		document.getElementById('pic_div').innerHTML = "";
	}
	document.getElementById('pic_div').appendChild(img);
});