var paper = Snap('#paper');

//marks cubes
var rect = paper.rect(10, 10, 30, 30).attr({fill:'green'});
var rect = paper.rect(1880, 10, 30, 30).attr({fill:'green'});
var rect = paper.rect(1880, 5960, 30, 30).attr({fill:'green'});
var rect = paper.rect(10, 5960, 30, 30).attr({fill:'green'});


//Snap.load("/static/images/svg/device.svg", onDeviceLoaded);
//Snap.load("/static/images/svg/hand.svg", onHandLoaded);
Snap.load("https://res.cloudinary.com/hrd77vjei/image/upload/v1657825425/svg/device.svg", onDeviceLoaded);
Snap.load("https://res.cloudinary.com/hrd77vjei/image/upload/v1657825425/svg/hand.svg", onHandLoaded);

function onDeviceLoaded(svg){ 

    var pos = new Snap.Matrix();
    pos.translate(700,300).scale(1.5,1.5);

    var g = paper.group(
        svg.select('#Border'),
        svg.select('#Base'),
        svg.select('#TextLayer')
    );

    g.attr({id:'device'}).transform(pos);
    paper.add(g);

    var border = paper.select('#Border');
    var textLayer = paper.select('#TextLayer');

    var mask = paper.select('#Mask');
    g.group(textLayer).attr({mask:mask});
    
    var anim1 = function() {
        var bbox = border.getBBox();
        var t = new Snap.Matrix();
        t.scale(1.2,1.2,bbox.cx, bbox.cy);
        border.animate({ transform: t}, 1700, mina.easeinout, anim2);
    };
    var anim2 = function() {
        var bbox = border.getBBox(); 
        var t = new Snap.Matrix();
        t.scale(1,1,bbox.cx, bbox.cy);
        border.animate({ transform: t}, 1700, mina.easeinout, anim1);
    };
    var anim3 = function(){
        var t = new Snap.Matrix();
        t.translate(-100, 55);
        //t.add(textLayer.transform().localMatrix);
        textLayer.animate({ transform: t }, 500, mina.easeinout);
    };
    var anim4 = function(){
        var t = new Snap.Matrix();
        t.translate(0, 0);
        textLayer.animate({ transform: t }, 500, mina.easeinout);
    };

    anim1();
    $('#device').on({
        mouseenter: anim3,
        mouseleave: anim4
    });
}
function onHandLoaded(svg){
    var pos = new Snap.Matrix();
    pos.translate(1100,1000).scale(3,3);

    var little = svg.select('#little');
    var ring = svg.select('#ring');
    var index = svg.select('#index');
    var middle = svg.select('#middle');
    var metacarpus = svg.select('#metacarpus');
    var thumb = svg.select('#thumb');

    var g = paper.group(little,ring,index,middle,metacarpus,thumb);

    g.attr({id:'hand'}).transform(pos);
    paper.add(g);

    var anim1 = function() {
        var t = new Snap.Matrix();
        t.rotate(2,thumbBBox.cx+40, thumbBBox.cy-18);
        
        thumb.animate({ transform: t}, 3400, mina.easeinout, anim2);
    };
    var anim2 = function() {
        var t = new Snap.Matrix();
        t.rotate(-2,thumbBBox.cx+40, thumbBBox.cy-18);
        thumb.animate({ transform: t}, 3400, mina.easeinout, anim1);
    };
    var anim3 = function() {
        var t = new Snap.Matrix();
        t.rotate(1,middleBBox.cx-3, middleBBox.cy-52);
        
        middle.animate({ transform: t}, 2500, mina.easeinout, anim4);
    };
    var anim4 = function() {
        var t = new Snap.Matrix();
        t.rotate(-1,middleBBox.cx-3, middleBBox.cy-52);
        middle.animate({ transform: t}, 2500, mina.easeinout, anim3);
    };
    var anim5 = function() {
        var t = new Snap.Matrix();
        t.rotate(1,ringBBox.cx+10, ringBBox.cy-52);
        
        ring.animate({ transform: t}, 5200, mina.easeinout, anim6);
    };
    var anim6 = function() {
        var t = new Snap.Matrix();
        t.rotate(-1,ringBBox.cx+10, ringBBox.cy-52);
        ring.animate({ transform: t}, 5200, mina.easeinout, anim5);
    };
    var anim7 = function() {
        var t = new Snap.Matrix();
        t.rotate(3,littleBBox.cx, littleBBox.cy-32);
        
        little.animate({ transform: t}, 7300, mina.easeinout, anim8);
    };
    var anim8 = function() {
        var t = new Snap.Matrix();
        t.rotate(-3,littleBBox.cx, littleBBox.cy-32);
        little.animate({ transform: t}, 7300, mina.easeinout, anim7);
    };

    var thumbBBox = thumb.getBBox();
    var middleBBox = middle.getBBox();
    var ringBBox = ring.getBBox();
    var littleBBox = little.getBBox();
    anim1();
    anim3();
    anim5();
    anim7();
}