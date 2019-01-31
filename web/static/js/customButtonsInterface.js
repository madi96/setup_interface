
var rewardDefaultTransform;
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
	var module = infoList[0];
	if (module == "redButton"){
	    module = svgDocument.getElementById("svgInterface").getElementById(module);
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#d40000ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "blueButton"){
	    module = svgDocument.getElementById("svgInterface").getElementById(module);
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#0000ffff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "yellowButton"){
	    module = svgDocument.getElementById("svgInterface").getElementById(module);
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#ffff00ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "greenButton"){
	    module = svgDocument.getElementById("svgInterface").getElementById(module);
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#00ff00ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	    
	} else if (module == "squarGreenButton"){
	    module = svgDocument.getElementById("svgInterface").getElementById(module);
	    if (infoList[1].toLowerCase() == "on"){module.style.fill = "#00ff00ff";}
	    else if (infoList[1].toLowerCase() == "off"){module.style.fill = "#37483e";} 
	} else if (module == "reward"){
	    var reward = svgDocument.getElementById("svgInterface").getElementById('reward');
	    var newState = rewardDefaultTransform +'translate('+(infoList[1]*0).toString()+','+(infoList[1]*-310).toString()+')';
	    reward.setAttribute('transform', newState);
	    
	}

	}
	

};
