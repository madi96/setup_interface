var joystickDefaultTransform;
var leverDefaultTransform;
var rewardDefaultTransform;
var smiling;
var happy;
var confused;
var sad;
var unhappy;
function setToDefault(){
    svgDocument = document.getElementById("svgInterface").contentDocument;
    // Get default jostick transform
    var joystick_center = svgDocument.getElementById("svgInterface").getElementById('joystick_center');
    joystickDefaultTransform =  joystick.getAttribute('transform')
    // Get default lever transform
    var lever = svgDocument.getElementById("svgInterface").getElementById('lever');
    leverDefaultTransform =  lever.getAttribute('transform')
    // Get default reward transform
    var reward = svgDocument.getElementById("svgInterface").getElementById('reward');
    rewardDefaultTransform =  reward.getAttribute('transform')
    
}

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
    var joystick_center = svgDocument.getElementById("svgInterface").getElementById('joystick_center');
    joystickDefaultTransform =  joystick_center.getAttribute('transform')
    // Get default lever transform
    var lever = svgDocument.getElementById("svgInterface").getElementById('lever');
    leverDefaultTransform =  lever.getAttribute('transform')
    // Get default reward transform
    var reward = svgDocument.getElementById("svgInterface").getElementById('reward');
    rewardDefaultTransform =  reward.getAttribute('transform')
	// svgDoc=document.getElementById("svgInterface").contentDocument;
	// button=svgDoc.getElementById("svgInterface").getElementById("button");
    }
    
    
    ws.onclose = function(e) { }
    
    ws.onmessage = function(info) {
	svgDocument = document.getElementById("svgInterface").contentDocument;
	//setToDefault();
	//alert("new message arrived"+ info.data)
	var infoList = info.data.split(":");
	var type = infoList[0];
	if (type == "button"){
	    var button = svgDocument.getElementById("svgInterface").getElementById(type);
	    if (infoList[1].toLowerCase() == "on"){button.style.fill = "#008000ff";}
	    else if (infoList[1].toLowerCase() == "off"){button.style.fill = "#d40000ff";} 
	} 
	else if (type == "joystick"){
	    var joystick = svgDocument.getElementById("svgInterface").getElementById('joystick_center');
	    var newState = joystickDefaultTransform+'translate('+(infoList[1]*900).toString()+','+(infoList[2]*900).toString()+')';
	    joystick.setAttribute('transform', newState);
	}
	
	else if (type == "lever"){
	    var lever = svgDocument.getElementById("svgInterface").getElementById('lever');
	    var newState = leverDefaultTransform +'translate('+(infoList[1]*170).toString()+')';
	    lever.setAttribute('transform', newState);

	}

	else if (type == "reward"){
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
