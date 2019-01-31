var rewardDefaultTransform;
window.onload = function() {
    var ws = new WebSocket("ws://localhost:8888/ws");
    ws.onopen = function(e) {
    svgDocument = document.getElementById("svgInterface").contentDocument;
    // Get default reward transform
    var reward = svgDocument.getElementById("svgInterface").getElementById('reward');
    rewardDefaultTransform =  reward.getAttribute('transform');
	
    // set box to close
    var box_top = svgDocument.getElementById("svgInterface").getElementById('box_opened');
    // svgDoc=document.getElementById("svgInterface").contentDocument;
    // button=svgDoc.getElementById("svgInterface").getElementById("button");
    // alert("mammaia    "+svgDoc);
    }
     
    ws.onclose = function(e) { }
    
    ws.onmessage = function(info) {
	svgDocument = document.getElementById("svgInterface").contentDocument;
	//setToDefault();
	//alert("new message arrived"+ info.data)
	var info_list = info.data.split(":");
	var module = info_list[0];
	if (module == "box"){
	    var box_status = info_list[1];
	    var box_closed = svgDocument.getElementById("svgInterface").getElementById('box_closed');
	    var box_opened = svgDocument.getElementById("svgInterface").getElementById('box_opened');
	    if (box_status.toLowerCase() == "open") {
		box_closed.setAttribute("visibility", "hidden");
		box_opened.setAttribute("visibility", "visible");
	    } else if  (box_status.toLowerCase() == "close") {
		box_opened.setAttribute("visibility", "hidden");
		box_closed.setAttribute("visibility", "visible");
	    }
	    
	}else if (type == "reward"){
	    var reward = svgDocument.getElementById("svgInterface").getElementById('reward');
	    var newState = rewardDefaultTransform +'translate('+(infoList[1]*0).toString()+','+(infoList[1]*-310).toString()+')';
	    reward.setAttribute('transform', newState);
	}
	
    }

};
