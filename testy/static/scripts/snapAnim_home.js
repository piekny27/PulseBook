var paper = Snap('#paper');

//marks cubes
var rect = paper.rect(10, 10, 30, 30).attr({fill:'green'});
var rect = paper.rect(1880, 10, 30, 30).attr({fill:'green'});
var rect = paper.rect(1880, 5960, 30, 30).attr({fill:'green'});
var rect = paper.rect(10, 5960, 30, 30).attr({fill:'green'});


Snap.load("/static/images/svg/device.svg", onDeviceLoaded);

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