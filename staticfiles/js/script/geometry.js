function these_colors(){
    colors = ["orangered","sienna","brown","sienna","orangered","orangered","orangered","ivdarkkhaki","darkseagreen","royalblue","navy","royalblue"] 
    bgcolors = ["tomato","salmon","coral","lightcoral","linen","bisque","blanchedalmond","ivory","honeydew","seashell","peachpuff","lightsteelblue"]

    max = colors.length ;
    let i = Math.floor(Math.random() * max);
    var color = { }
    color['contour'] = colors[ i ] ;
    color['bg'] = bgcolors[ i ] ;
    return color
} 

// fonction de construction
function deg_to_rad(degrees){
  var pi = Math.PI;
  return degrees * (pi/180);
}

// fonction de construction
function drawWedge(w,fill,stroke,index){
    const canvas = document.getElementById("canvas"+index);
    const ctx = canvas.getContext("2d");
    ctx.beginPath(); 
    ctx.moveTo(w.cx, w.cy);
    ctx.arc(w.cx, w.cy, w.radius, w.startAngle, w.endAngle);
    ctx.closePath();
    ctx.fillStyle=fill;
    ctx.fill();
    ctx.strokeStyle=stroke;
    ctx.stroke();
}

// fonction d'appel
function pizza(n,d,index){
    var nalea = 1+Math.floor(Math.random() * (n-1));
    const color = these_colors() ;    
    const canvas = document.getElementById("canvas"+index);
    let theta = Math.floor(360/d);
    let loop = 1+Math.floor(nalea/d);  
    let i=0;
    let j=0;
    let m=0;
    let maxi=Math.max(nalea,d);  
    if (canvas.getContext) {
      const ctx = canvas.getContext("2d");
      ctx.beginPath();
      if (nalea%d != 0){
        while (m < loop) {
          ctx.moveTo(100+175*m,100);    
          ctx.arc(100+175*m, 100 , 75, 0, 2 * Math.PI);

          for (var s=0;s<d;s++){
            var a = 2*Math.PI* s/d ;
            ctx.moveTo(100+175*m,100);     
            ctx.lineTo(100+175*m + 75*Math.cos(a), 100-75*Math.sin(a));
          }
          ctx.stroke();
          m++;
        }
      }     
      while (i < maxi) {      
        var l = Math.floor(i/d);
        var a = deg_to_rad( i*theta );
        var b = deg_to_rad( (i+1)*theta );
        var wedge={cx:100+175*l, cy:100 ,radius:75,startAngle:a,endAngle:b}; 
        if (i<nalea) { drawWedge(wedge, color.bg , color.contour, index );}   
        ctx.stroke();
        i++;
      }  

    }
  }
 

// fonction de construction
function rectangle(a,b,w, f,color,index) {
  var canvas = document.getElementById("canvas"+index); 
  var context = canvas.getContext("2d");
  context.beginPath(); 
  context.strokeStyle=color.c;   
  context.lineWidth="2";   
  context.rect(a,b,w,50); 
  if(f==1){
  context.fillStyle=color.bg;
  context.fill();}
  context.stroke();
}
// fonction d'appel
function chocolat(n,d,format,index){
    var nalea = 1+Math.floor(Math.random() * (n-2));
    const color = these_colors() ;
    if (format == 0){ var q = d ;} else { var q = format;}
      let i = 0 ;
      let k = 0 ;
      let j = 0 ;
      let f = 0;
      let width = Math.floor(650/q);
      let l = Math.floor(nalea/d);
      m = Math.max(nalea,d);
      while (i < m){
          let ord = Math.floor(i/q);
          if (i<nalea) { f = 1 ;} else {f=0;} 
          abs = i%q;
          rectangle( 125+width*abs, 50+ 50*ord, width , f,color,index);
          i++;
      }   
}

// fonction de construction
function thales_voile(index){
    let i = 130 + Math.floor(Math.random()*6)*100;
    let j = 0.2 + Math.random()*0.6;
    let k = Math.floor(Math.random()*3);
    k=2;
    var canvas = document.getElementById("canvas"+index);
    var ctx = canvas.getContext("2d");
    ctx.beginPath();
    ctx.font = '25px Arial';    
    ctx.linewidth="2";
    xA = i , yA = 50 ;
    xB = 150 , yB = 350 ;
    xC = 650 , yC = 350 ;
    ctx.moveTo(xA,yA); //coord de A
    ctx.lineTo(650,350);
    ctx.moveTo(i,50);
    ctx.lineTo(xB,yB); 
    ctx.moveTo(150,350);
    ctx.lineTo(xC,yC);
    ctx.fillText('A', xA, yA-5);
    ctx.fillText('B', xB-20, yB);
    ctx.fillText('C', xC+10, yC);
    if(k==0){
        xD = xB+(xA-xB)*j;
        yD = yB+(yA-yB)*j;
        xE = xC+(xA-xC)*j;
        yE = yC+(yA-yC)*j;
        ctx.fillText('D', xD-20, yD);
        ctx.fillText('E', xE+10, yE); 
        ctx.moveTo(xD-20,yD);
        ctx.lineTo(xE+20,yE);
        ctx.font = '15px Arial';
        ctx.fillText('Les droites (BC) et (ED) sont parallèles.', 20, 430);
    }
    else if(k==1){
        xD = xA+(xC-xA)*j;
        yD = yA+(yC-yA)*j;
        xE = xB+(xC-xB)*j;
        yE = yB+(yC-yB)*j;
        ctx.fillText('D', xD+10, yD+10);
        ctx.fillText('E', xE, yE+20); 
        ctx.moveTo(xD,yD);
        ctx.lineTo(xE,yE);  
        ctx.font = '15px Arial';
        ctx.fillText('Les droites (AB) et (ED) sont parallèles.', 20, 430);
    }
    else{
        xD = xA+(xB-xA)*j;
        yD = yA+(yB-yA)*j;
        xE = xC+(xB-xC)*j;
        yE = yC+(yB-yC)*j;
        ctx.fillText('D', xD-20, yD);
        ctx.fillText('E', xE, yE+20); 
        ctx.moveTo(xD,yD);
        ctx.lineTo(xE,yE);  
        ctx.font = '15px Arial';
        ctx.fillText('Les droites (AC) et (ED) sont parallèles.', 20, 430);
    }
    ctx.stroke();    
    ctx.closePath();
}
// fonction de construction
function thales_papillon(index){
    let i = 90 + Math.floor(Math.random()*5)*50;
    let k = 400 + Math.floor(Math.random()*4)*50;
    let j = Math.floor(Math.random()*5)*30;
    var canvas = document.getElementById("canvas"+index);
    var ctx = canvas.getContext("2d");
    ctx.beginPath();
    ctx.strokeStyle = '#000'
    ctx.moveTo(80,80);
    ctx.lineTo(750,400);
    ctx.moveTo(50,350);    
    ctx.lineTo(735,100);
    ctx.stroke();
    ctx.closePath();
    ctx.beginPath();
    ctx.strokeStyle = '#ff0000'
    ctx.moveTo(i+j,375);    
    ctx.lineTo(i,75);
    ctx.moveTo(k+j,375);
    ctx.lineTo(k,75);
    ctx.font = '15px Arial';  
    ctx.fillText('Les droites sont parallèles.', 20, 430);
    ctx.stroke();
}
// fonction d'appel
function thales(p,index){
    if (p==0){ 
        let j = Math.floor(Math.random()*2);
        if (j==0) {thales_voile(index) ; } else { thales_papillon(index) ; }
    }
    else if (p==0){ thales_voile(index) ; }
    else { thales_papillon(index) ; }   
}


// fonction d'appel
function pythagore(a,index){
    let p = Math.floor(Math.random()*4);
    var canvas = document.getElementById("canvas"+index);
    var ctx = canvas.getContext("2d");
    ctx.beginPath();
    if (p == 0) {
        ctx.moveTo(150,300);
        ctx.lineTo(550,300);   
        ctx.lineTo(443,123);
        ctx.lineTo(150,300);
        ctx.moveTo(427,132);
        ctx.lineTo(436,147);
        ctx.lineTo(451,138);
        ctx.font = '25px Arial';
        ctx.fillText('A', 140, 320); 
        ctx.fillText('B', 550, 320);
        ctx.fillText('C', 450, 130);
    }
    else if (p == 1) {
        ctx.moveTo(150,300);
        ctx.lineTo(550,300);   
        ctx.lineTo(253,125);
        ctx.lineTo(150,300);
        ctx.moveTo(246,138);
        ctx.lineTo(258,145);
        ctx.lineTo(266,132);
        ctx.font = '25px Arial';
        ctx.fillText('A', 140, 320); 
        ctx.fillText('B', 550, 320);
        ctx.fillText('C', 253, 124);
    }
    else if (p == 2) {
        ctx.moveTo(150,300);
        ctx.lineTo(550,300);   
        ctx.lineTo(150,125);
        ctx.lineTo(150,300);
        ctx.moveTo(160,300);
        ctx.lineTo(160,290);
        ctx.lineTo(150,290);
        ctx.font = '25px Arial';
        ctx.fillText('A', 140, 320); 
        ctx.fillText('B', 550, 320);
        ctx.fillText('C', 143, 124);
    }
    else if (p == 3) {
        ctx.moveTo(150,300);
        ctx.lineTo(550,300);   
        ctx.lineTo(550,125);
        ctx.lineTo(150,300);
        ctx.moveTo(540,300);
        ctx.lineTo(540,290);
        ctx.lineTo(550,290);
        ctx.font = '25px Arial';
        ctx.fillText('A', 140, 320); 
        ctx.fillText('B', 550, 320);
        ctx.fillText('C', 553, 120);
    }   
    ctx.stroke();
}

// fonction d'appel
function abscisse(start,end,tick,subtick,index){
 
    var canvas = document.getElementById("canvas"+index);
    var ctx = canvas.getContext("2d");

    var canvas_cor = document.getElementById("canvas_corrector"+index); 
    var canvas_cor = document.getElementById("canvas_corrector"+index);  

    //Conversion des pixels à la droite graduée
    var unit = (end - start)/tick ; 
    var tck = 600/unit;    // en pixel     
    var sbtck = tck/subtick; // sous graduation  en pixel
    var nb_total_graduation = unit * subtick ; // sous graduation  en pixel


    var alea = Math.floor(Math.random()*nb_total_graduation)
    var p = 150 + alea * (60/subtick);

    console.log(nb_total_graduation + " " + subtick+ " " + alea+ " " + (60/subtick) + " " + p )

 

    abscisse_ctx(start,end,tick,tck,sbtck,ctx,100,p) ;
    if(canvas_cor) {var ctx_cor = canvas_cor.getContext("2d");
        abscisse_ctx(start,end,tick,tck,sbtck,ctx_cor,0,p) ;}
   
    document.getElementById("answer_cor"+index).innerText = (start + (p-150)/sbtck/subtick).toString().replace(".",",") ; 

    var ipt = document.createElement("input");
    ipt.setAttribute("type", "hidden");
    ipt.setAttribute("name", "origin"+index);
    ipt.setAttribute("value", start);
    canvas.appendChild(ipt);

    var inpt = document.createElement("input");
    inpt.setAttribute("type", "hidden");
    inpt.setAttribute("name", "unit"+index);
    inpt.setAttribute("value", unit);
    canvas.appendChild(inpt);

    var input = document.createElement("input");
    input.setAttribute("type", "hidden");
    input.setAttribute("name", "value"+index);
    input.setAttribute("value", p);
    canvas.appendChild(input);


    var inputs = document.createElement("input");
    inputs.setAttribute("type", "hidden");
    inputs.setAttribute("name", "sbtck"+index);
    inputs.setAttribute("value", sbtck);
    canvas.appendChild(inputs);

    var inputf = document.createElement("input");
    inputf.setAttribute("type", "hidden");
    inputf.setAttribute("name", "format"+index);
    inputf.setAttribute("value", "pizza");
    canvas.appendChild(inputf);
}



function abscisse_ctx(start,end,tick,tck,sbtck,ctx,top,p){


    ctx.beginPath();
    // Tracé de l'axe
    ctx.moveTo(150,top+50);
    ctx.lineTo(750,top+50);   
    //graduation
    ctx.font = '25px Arial';
    ctx.fillText(start, 142, top+36);
    ctx.fillText(end, 735, top+36);
    ctx.fillText(start + tick, 142+tck, top+36);   

    var a = 150; // abscisses de la graduation tick
    var b = 150; // abscisses de la graduation subtick
    ctx.moveTo(a,top+40); // haut de la graduation
    ctx.lineTo(a,top+60); // bas de la graduation

    while (a<750){
        a = a + sbtck;
        ctx.moveTo(a,top+45);
        ctx.lineTo(a,top+55);
    }
    while (b<750){
        b = b + tck;
        ctx.moveTo(b,top+40);
        ctx.lineTo(b,top+60);
    }
    ctx.stroke();
    ctx.closePath();
    // fin de la graduation
    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.fillStyle = "red"; 
    ctx.font = '30px Arial'; 
    if (sbtck==10)
    {ctx.fillText('|', p - 0.5*sbtck , top+60);
        ctx.fillText('|', p - 0.5*sbtck , top+96);
        ctx.fillText('^', p - 1*sbtck , top+96); }
    else
    {ctx.fillText('|', p - 3  , top+60);
        ctx.fillText('|', p - 3  , top+96);
        ctx.fillText('^', p  - 6 , top+96); }  

    ctx.stroke();
    ctx.closePath();

}