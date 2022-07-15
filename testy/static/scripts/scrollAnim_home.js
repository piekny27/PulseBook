const html = document.documentElement;
const canvas = document.getElementById("renderCanvas");
const context = canvas.getContext("2d");
const firstScreen = document.getElementById("firstScreen");

const frameCount = 148;
const currentFrame = index => (
  //`https://res.cloudinary.com/hrd77vjei/image/upload/v1657226679/anim/01-light-rim/${index.toString().padStart(4, '0')}.png`
  `/static/images/01-light-rim/${index.toString().padStart(4, '0')}.png`
)

var handEvent = false;
var handAnim = false;
const img = new Image()
img.src = currentFrame(1);
canvas.width=1158;
canvas.height=770;
img.onload=function(){
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.drawImage(img, 0, 0);
}

const preloadImages = () => {
  for (let i = 1; i < frameCount; i++) {
    const img = new Image();
    img.src = currentFrame(i);
  }
};

const updateImage = index => {
  img.src = currentFrame(index);
  context.drawImage(img, 0, 0);
}

function map_range(value, low1, high1, low2, high2) {
  return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}

function setBgColor(scrollValue){
  const [red, green, blue] = [12, 20, 48]; //default
  const [red2, green2, blue2] = [108, 142, 180]; //blue dragon
  var y = 1;
  if(scrollValue<0.76) y=map_range(scrollValue,0,0.76,40,1);
  else y=1;
  const [r, g, b] = [red/y, green/y, blue/y].map(Math.round);
  const [r2, g2, b2] = [red2/y, green2/y, blue2/y].map(Math.round);
  firstScreen.style.background = `radial-gradient(circle, rgb(${r2}, ${g2}, ${b2}) 0%,rgb(${r}, ${g}, ${b}) 65%, rgb(${r}, ${g}, ${b}) 100%)`
}

function animText(scrollValue, elementID, startScroll, stopScroll){
  const text1 = document.getElementById(elementID);
  text1.style.display = 'block';
  if(scrollValue>startScroll && scrollValue<stopScroll){
    y=map_range(scrollValue,startScroll,stopScroll,40,-40);
    if(scrollValue>startScroll && scrollValue < startScroll + ((stopScroll-startScroll)/3))
    {
      text1.style.opacity=map_range(scrollValue,startScroll,startScroll + ((stopScroll-startScroll)/3),0,1);
    }
    if(scrollValue>startScroll + ((stopScroll-startScroll)/3) && scrollValue < startScroll + 2*((stopScroll-startScroll)/3))
    {
      text1.style.opacity=1;
    }
    if(scrollValue>startScroll + 2*((stopScroll-startScroll)/3) && scrollValue < startScroll + 3*((stopScroll-startScroll)/3))
    {
      text1.style.opacity=map_range(scrollValue,startScroll+ 2*((stopScroll-startScroll)/3),startScroll + 3*((stopScroll-startScroll)/3),1,0);
    }
    text1.style.transform=`translate(-50%, calc(-50% + ${y}px))`;
  }
  else{
    text1.style.display = 'none';
  }
}

function animRenderOut(scrollValue){
  if(scrollValue>0.9){
    y=map_range(scrollValue,0.9,1.4,-50,-200);
    canvas.style.transform=`translate(-50%,${y}%)`;
  }else
  {
    canvas.style.transform=`translate(-50%,-50%)`;
  };
};

function animBrandTextOut(scrollValue){
  const brandText = document.getElementById("brandText");
  if(scrollValue<0.5){
    y=map_range(scrollValue,0,0.5,0,-200);
    brandText.style.transform=`translateY(calc(-40vh - ${y}px))`;
  };
};

function loadFollower()
{
  window.onload = function() {
    TweenMax.set('.follower', {xPercent: -50, yPercent: -50});
    const cont = document.getElementById("main");
    cont.addEventListener('mousemove', e => {
        const follower = document.getElementsByClassName("follower");
        TweenMax.to(follower, 0.8, {
        x: e.clientX,
        y: e.clientY,
        ease:Power4.easeOut
        });
    });
  }; 
}

function animHand(){
  const hand = document.getElementById("hand");
  if(!hand) return;
  
  var bRect = hand.getBoundingClientRect(); 
  var p = bRect.top + (bRect.height/2)-(window.innerHeight/2);
  scrollValue=map_range(p,100,300,4.2,3.9);

  if(scrollValue>3.9 && scrollValue<4.2){
    var h = paper.select('#hand');
    x=map_range(scrollValue,3.9,4.2,0,-250);
    var t = new Snap.Matrix();
    t.translate(1100+x, 1000).scale(3,3);
    h.transform(t);
    handEvent=true;
  }
  else if(scrollValue>=4.2){
    var h = paper.select('#hand');
    var t = new Snap.Matrix();
    t.translate(850, 1000).scale(3,3);
    h.transform(t);
    if(handEvent && !handAnim){
      //console.log('start async handEvent');
      var deviceAnim = async function() {
        const wait = (seconds = 1) => new Promise((r) => setTimeout(r, seconds * 1e3));
        const clearChildren = function(ch){
          ch.forEach(function( el ) {
            var bbox = el.getBBox();
            var t = new Snap.Matrix();
            t.scale(0,0,bbox.cx, bbox.cy);
            el.attr({ transform: t });
          });
        };

        handAnim = true;
        var loadingChildren = paper.select('#loading').selectAll('g');
        paper.select('#done').attr({opacity:0});
        clearChildren(loadingChildren);

        for(var i=0; i<loadingChildren.length; i++){
          if(scrollValue<4.2){
            handAnim=false;
            return "Aborded"
          ;}
          var bbox = loadingChildren[i].getBBox();
          var t = new Snap.Matrix();
          t.scale(1,1,bbox.cx, bbox.cy);
          loadingChildren[i].animate({ transform: t}, 300, mina.elastic);
          await wait(0.5);
        }

        clearChildren(loadingChildren);
        paper.select('#done').attr({opacity:1});
        handAnim=false;
        return "Done";
      }
      
      deviceAnim().then(
        function(value) {
          //console.log(value);
        },
        function(error) {console.log(error);}
      );
    }
    handEvent=false;
  }
}

function loadScroll(){
  window.addEventListener('scroll', () => {  
    const scrollTop = html.scrollTop;
    const maxScrollTop = firstScreen.scrollHeight - window.innerHeight;
    const scrollFraction = scrollTop / maxScrollTop;
    setBgColor(scrollFraction);
    animRenderOut(scrollFraction);
    animBrandTextOut(scrollFraction);
    animText(scrollFraction,'text1', 1.2, 1.9);
    animText(scrollFraction,'text2', 1.9, 2.6);
    animText(scrollFraction,'text3', 2.6, 3.3);
    animHand();
    //console.log(scrollFraction);
    const frameIndex = Math.min(
      frameCount - 1,
      Math.ceil(scrollFraction * frameCount)
    );
    requestAnimationFrame(() => updateImage(frameIndex + 1))
  });
}

$("#renderCanvas").delay(200).fadeTo(1500,1);
$("#brandText").delay(1000).fadeTo(2000,1);
$("#firstScreen").addClass('grain');
loadScroll();
preloadImages();
loadFollower(); 



