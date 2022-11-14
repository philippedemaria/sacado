var tab=document.getElementById("tableau");
var xoffset=tab.offsetTop;
var yoffset=tab.offsetLeft;

var axe=document.getElementById("axe");

var xmin=document.getElementById("xmin");
var xmax=document.getElementById("xmax");
var graduation=document.getElementById("graduation");
var precision =document.getElementById("precision");

//   dessin des graduations de l'axe 
function placeValeur(x) {  
   // position en pixels, en fonction de la valeur x
   x_axe=Math.round((x-xmin)/(xmax-xmin) * axe.offsetWidth);
   
   // creation du label : le texte de la valeur à afficher 
   label=document.createElement("div");
   label.textContent=x.toString();
   label.style.position="absolute";
   label.style.top  = "-40px";
   axe.appendChild(label);
   label.style.text_align="center";
   label.style.left = x_axe-label.offsetWidth/2+"px";
   // le "tick" = la graduation 
   tick= document.createElement("div");
   tick.style.position="absolute";
   tick.style.top  = label.offsetTop + label.offsetHeight ;
   tick.style.height= -label.offsetTop - label.offsetHeight 
   tick.style.width="0px";
   tick.style.border="1px solid";
   tick.style.left = x_axe+"px";
   axe.appendChild(tick);
   
   
}

function dessineGraduations(){
    for (x=xmin; x< xmax ;x = x+ graduation ) 
        {placeValeur(x)}
    placeValeur( xmax );
}
dessineGraduations();

cartes=Array();
var topz=$(".carte").length ; 

for (i=0;i < topz ;i++) {	
	c=document.getElementById("carte"+i.toString());
	if (i==0) {var rect = c.getBoundingClientRect();}
	console.log("rect:",rect.top);
	c.style.top = 300+yoffset + (i)*10 + "px";
	c.style.left =xoffset + (i)*50 + "px";
	c.style.zIndex=i;
	cartes.push(c);
	AssociationEvnt(cartes[i]);
}
// le niveau de la couche la plus haute


function AssociationEvnt(carte) {
  var X=0, Y=0,dernierX = 0, dernierY = 0;
  carte.onmousedown = (e) => dragMouseDown(carte,e);
  //carte.onmouseout  =  (e)=> closeDragElement(carte)
  // clic droit : on détache la carte de l'axe
  carte.oncontextmenu = (e)=> {
	   if (carte.childNodes.length>=3) {carte.removeChild(carte.childNodes[2])}
	   carte.childNodes[1].innerHTML="";
   }
  }

  function dragMouseDown(carte,e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    carte.style.zIndex=topz;
	topz=topz+1;
  
    dernierX = e.clientX;
    dernierY = e.clientY;
    carte.onmouseup = (e) => closeDragElement(carte);
    // call a function whenever the cursor moves:
    carte.onmousemove = (e) => elementDrag(carte,e);
  }

  function elementDrag(carte,e) {
	nc=parseInt(carte.id.substring(5));
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    X = dernierX - e.clientX;
    Y = dernierY - e.clientY;
    dernierX = e.clientX;
    dernierY = e.clientY;
    // set the element's new position:
    carte.style.top = Math.min(tableau.offsetHeight,
                        Math.max (axe.offsetTop+10,
                          (carte.offsetTop - Y))) + "px";
    w=carte.offsetWidth/2;  
    carte.style.left = Math.max(axe.offsetLeft-w,
                          Math.min (axe.offsetWidth+axe.offsetLeft-w,
                              carte.offsetLeft - X)) + "px";
    v=carte.childNodes[1];
        
    valeur=(xmin+(carte.offsetLeft+w-axe.offsetLeft)/axe.offsetWidth*(xmax-xmin));
    valeur=Math.round(valeur/precision)*precision;
    if (v.innerHTML==""){
        verticale=document.createElement("div");
        verticale.style.position="absolute";
        verticale.style.top=axe.offsetTop-carte.offsetTop;
        verticale.style.height=carte.offsetTop-axe.offsetTop;
        verticale.style.left=w;
        verticale.style.border="1px solid";
        carte.appendChild(verticale);
	}
	else 
	   {
		carte.lastChild.style.top=axe.offsetTop-carte.offsetTop;
        carte.lastChild.style.height=carte.offsetTop-axe.offsetTop;
	}
    v.innerHTML=valeur;
    
  }

  function closeDragElement(carte) {
    // stop moving when mouse button is released:
    carte.onmouseup = null;
    carte.onmousemove = null;
  }
