const html = document.documentElement;
const canvas = document.getElementById("renderCanvas");
const context = canvas.getContext("2d");
const firstScreen = document.getElementById("firstScreen");

const frameCount = 148;
const currentFrame = index => (
  `https://res.cloudinary.com/hrd77vjei/image/upload/v1657226679/anim/01-light-rim/${index.toString().padStart(4, '0')}.png`
  //`/static/images/01-light-rim/${index.toString().padStart(4, '0')}.png`
)

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
  firstScreen.style.background = `radial-gradient(circle, rgba(${r2}, ${g2}, ${b2}, 1) 0%,rgba(${r}, ${g}, ${b}, 1) 65%, rgba(${r}, ${g}, ${b}, 1) 100%)`
}

function animText(scrollValue, elementID, startScroll, stopScroll){
  const text1 = document.getElementById(elementID);
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
    text1.style.opacity=0;
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
    brandText.style.transform=`translateY(${y}px)`;
  };
};

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
  console.log(scrollFraction);
  const frameIndex = Math.min(
    frameCount - 1,
    Math.ceil(scrollFraction * frameCount)
  );
  
  requestAnimationFrame(() => updateImage(frameIndex + 1))
});

$("#renderCanvas").delay(200).fadeTo(1500,1);
$("#brandText").delay(1000).fadeTo(2000,1);
preloadImages();

