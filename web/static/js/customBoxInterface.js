var rewardDefaultTransform;
var smiling;
var happy;
var confused;
var sad;
var unhappy;

function setSmileysToDefault(){
		svgDocument = document.getElementById("svgInterface").contentDocument;
		smiling = svgDocument.getElementById("svgInterface").getElementById('smiling');
		happy = svgDocument.getElementById("svgInterface").getElementById('happy');
 		confused = svgDocument.getElementById("svgInterface").getElementById('confused');
		sad = svgDocument.getElementById("svgInterface").getElementById('sad');
		unhappy = svgDocument.getElementById("svgInterface").getElementById('unhappy');
		
		
		//set to default
		smiling.setAttribute("visibility", "hidden");
		happy.setAttribute("visibility", "hidden");
		confused.setAttribute("visibility", "visible");
		sad.setAttribute("visibility", "hidden");
		unhappy.setAttribute("visibility", "hidden");
 	}


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
	    
	} else if (module == "reward"){
		var translate_value = infoList[1];
	    var reward = svgDocument.getElementById("svgInterface").getElementById('reward');
	    var newState = rewardDefaultTransform +'translate('+(translate_value*0).toString()+','+(translate_value*-310).toString()+')';
	    reward.setAttribute('transform', newState);
	    setSmileysToDefault();
	    if (translate_value >= -1 && translate_value < -0.5){
			confused.setAttribute("visibility", "hidden");
			unhappy.setAttribute("visibility", "visible");
		} else if  (translate_value >= -0.5 && translate_value < 0){
			confused.setAttribute("visibility", "hidden");
			sad.setAttribute("visibility", "visible");
		} else if  (translate_value > 0 && translate_value < 0.5){
			confused.setAttribute("visibility", "hidden");
			smiling.setAttribute("visibility", "visible");
		} else if  (translate_value >= 0.5 && translate_value <= 1){
			confused.setAttribute("visibility", "hidden");
			happy.setAttribute("visibility", "visible");
		}
	}
    }
};
