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
	// svgDoc=document.getElementById("svgInterface").contentDocument;
	// button=svgDoc.getElementById("svgInterface").getElementById("button");
	// alert("mammaia    "+svgDoc);
    }
    
    
    ws.onclose = function(e) { }
    
    ws.onmessage = function(info) {
	svgDocument = document.getElementById("svgInterface").contentDocument;
	//setToDefault();
	//alert("new message arrived"+ info.data)
	var infoList = info.data.split(":");
	var module = infoList[0].toLowerCase();
	if (module == "redbutton"){
	    module = svgDocument.getElementById("svgInterface").getElementById("redButton");
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#d40000ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "bluebutton"){
	    module = svgDocument.getElementById("svgInterface").getElementById("blueButton");
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#0000ffff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "yellowbutton"){
	    module = svgDocument.getElementById("svgInterface").getElementById("yellowButton");
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#ffff00ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "greenbutton"){
	    module = svgDocument.getElementById("svgInterface").getElementById("greenButton");
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#00ff00ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "squargreenbutton"){
	    module = svgDocument.getElementById("svgInterface").getElementById("squarGreenButton");
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#00ff00ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
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
