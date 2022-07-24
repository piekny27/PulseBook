var paper = Snap('#paper');
var signEvent = false;

Snap.load("https://res.cloudinary.com/hrd77vjei/image/upload/v1657825425/svg/device.svg", onDeviceLoaded);
Snap.load("https://res.cloudinary.com/hrd77vjei/image/upload/v1657895424/svg/device2.svg", onDevice2Loaded);
Snap.load("https://res.cloudinary.com/hrd77vjei/image/upload/v1657825425/svg/hand.svg", onHandLoaded);
Snap.load("https://res.cloudinary.com/hrd77vjei/image/upload/v1657825425/svg/paths.svg", onPathsLoaded);
Snap.load("https://res.cloudinary.com/hrd77vjei/image/upload/v1658668889/svg/scene_art.svg", onSceneLoaded);

function randomRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min)
}
function onDeviceLoaded(svg){ 

    var pos = new Snap.Matrix();
    pos.translate(750,700).scale(1.5,1.5);

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
    pos.translate(1100,2900).scale(3,3);

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
function onDevice2Loaded(svg){
    var pos = new Snap.Matrix();
    pos.translate(-160,2715).scale(3,3);

    var cover = svg.select('#cover');
    var loading = svg.select('#loading');
    var text = svg.select('#done').attr({opacity:0});

    var g = paper.group(cover,loading,text);
    g.attr({id:'device2'}).transform(pos);
    

    var h = paper.select('#hand');
    if(h){ paper.add(g); paper.add(h); }
    else{ paper.add(g); }

    var loadingChildren = loading.selectAll('g');
    loadingChildren.forEach(function( el ) {
        var bbox = el.getBBox();
        var t = new Snap.Matrix();
        t.scale(0,0,bbox.cx, bbox.cy);
        el.attr({ transform: t });
    });
}
function onPathsLoaded(svg){
    var toggleClass = function(el,time){
        setInterval(async function(){
            var id =el.node.id.slice(-2);
            el.selectAll('path')[0].removeClass('animPath'+id+'1',0);
            el.selectAll('path')[1].removeClass('animPath'+id+'2',0);
            setTimeout(() => {
                el.selectAll('path')[0].addClass('animPath'+id+'1',1);
                el.selectAll('path')[1].addClass('animPath'+id+'2',1);
            }, 50);
        },time);
    }
    var pos = new Snap.Matrix();
    pos.translate(-50,-200).scale(1.5,1.5);
    var g1 = svg.select('#animPath01');
    //var g2 = svg.select('#animPath02');
    var g3 = svg.select('#animPath03');
    
    var gr = paper.group(g1,g3).attr({id:'snakes'}).transform(pos);
    paper.add(gr);
    toggleClass(g1,7000);
    //toggleClass(g2,4000);
    toggleClass(g3,12000);
}
function genSky(){
    var star = `M29.01,.36l7.74,21.8,17.36-1.89c1.83-.2,2.88,2.04,1.55,3.32l-14.66,14.07,4.25,
                12.93c.58,1.76-1.39,3.27-2.94,2.26l-14.06-9.19-15.32,16.14c-1.02,1.07-2.8,
                .16-2.54-1.29l3.61-19.85L.61,26.83c-1.27-1.13-.41-3.23,1.29-3.13l17.6,.97L27.99,
                .36c.17-.48,.85-.48,1.02,0Z`;
    var anim1 = async function(el,bbox,x,y) {
        var t = new Snap.Matrix();
        var s = randomRange(0.9,1.1).toFixed(2);
        var r = randomRange(-15,15);
        x = randomRange(50,1870);
        y = randomRange(50,800);
        el.transform('t'+x+' '+y).attr({opacity:0});  
        bbox = el.getBBox();
        t.scale(s,s,bbox.cx,bbox.cy);
        t.rotate(r,bbox.cx,bbox.cy);
        t.translate(x, y);
        el.animate({ transform: t,opacity:1}, randomRange(400,900), mina.linear, function(){anim2(el,bbox,x,y);});
    };
    var anim2 = function(el,bbox,x,y) {
        var t = new Snap.Matrix();
        var r = randomRange(-5,10);
        t.scale(0,0,bbox.cx,bbox.cy);
        t.rotate(r,bbox.cx,bbox.cy);
        t.translate(x, y);
        el.animate({ transform: t}, randomRange(10000,22000), (n)=>Math.pow(n, 5.7), function(){anim1(el,bbox,x,y)});
    };
    var anim3 = async function(el,bbox,x,y) {
        var t = new Snap.Matrix();
        var s = randomRange(0.5,1).toFixed(2);
        var r = randomRange(-15,15);
        x = randomRange(10,1910);
        y = randomRange(10,1200);
        el.transform('t'+x+' '+y).attr({opacity:0});  
        bbox = el.getBBox();
        t.scale(s,s,bbox.cx,bbox.cy);
        t.rotate(r,bbox.cx,bbox.cy);
        t.translate(x, y);
        el.animate({ transform: t,opacity:1}, randomRange(400,900), mina.linear, function(){anim4(el,bbox,x,y);});
    };
    var anim4 = function(el,bbox,x,y) {
        var t = new Snap.Matrix();
        var r = randomRange(-5,10);
        t.scale(0,0,bbox.cx,bbox.cy);
        t.rotate(r,bbox.cx,bbox.cy);
        t.translate(x, y);
        el.animate({ transform: t}, randomRange(10000,22000), (n)=>Math.pow(n, 5.7), function(){anim3(el,bbox,x,y)});   
    };
    
    var g = paper.group().attr({id:'sky'});
    var stars = g.group().attr({id:'stars'});
    for (let i = 0; i < 20; i++) {
        var x = randomRange(10,1910);
        var y = randomRange(10,1200);
        var s = stars.circle(0,0,10).attr({fill:'white',opacity:0});
        var b = s.getBBox();
        anim3(s, b, x, y);
    }
    for (let i = 0; i < 4; i++) {
        var x = randomRange(50,1870);
        var y = randomRange(50,800);
        var s = stars.path(star,200,200).attr({fill:'white'}).transform('t'+x+' '+y);  
        var b = s.getBBox();
        anim1(s, b, x, y);
    }
}
function onSceneLoaded(svg){
    var pos = new Snap.Matrix();
    pos.translate(-50,100).scale(1,1);

    var g = paper.group(
        svg.select('#widgets'),
        svg.select('#clouds'),
        svg.select('#scene'),
        svg.select('#user-friendly')
    );

    g.attr({id:'main_scene'}).transform(pos);
    paper.add(g);

    var heartBeatAnim = async function(){
        var heart = paper.select('#widgets-heart');
        var bbox = heart.getBBox();
        var t = new Snap.Matrix();
        heart.attr({transform:t});
        t.scale(0.9,0.9,bbox.cx, bbox.cy);
        var anim1 = function () {
            var t = new Snap.Matrix();
            t.scale(1.05,1.05,bbox.cx, bbox.cy);
            heart.animate({ transform: t}, 1400, mina.easeinout, anim2);
        }
        var anim2 = function () {
            var t = new Snap.Matrix();
            t.scale(0.9,0.9,bbox.cx, bbox.cy);
            heart.animate({ transform: t}, 1400, mina.easeinout, anim1);
        }
        anim1();
    }
    var handAnim = async function(){
        var hands = paper.select('#widgets-hands');
        var bbox = hands.getBBox();
        var anim1 = function () {
            var t = new Snap.Matrix();
            t.translate(0, -5);
            hands.animate({ transform: t}, 3000, mina.easeinout, anim2);
        }
        var anim2 = function () {
            var t = new Snap.Matrix();
            t.translate(0, 5);
            hands.animate({ transform: t}, 3000, mina.easeinout, anim1);
        }
        anim1();
    }
    var cloudsAnim = async function(){
        var cloud1 = paper.select('#clouds-cloud1');
        var cloud2 = paper.select('#clouds-cloud2');
        var cloud3 = paper.select('#clouds-cloud3');
        cloud1.attr({transform:'t-300 -25'});
        cloud2.attr({transform:'t-100 -5'});
        cloud3.attr({transform:'t200 -25'});

        var anim1 = function () {
            cloud1.animate({ transform: 't130 5'}, 90000, mina.linear, anim2);}
        var anim2 = function () {
            cloud1.animate({ transform: 't-300 -25'}, 90000, mina.linear, anim1);}
        var anim3 = function () {
            cloud2.animate({ transform: 't100 15'}, 110000, mina.linear, anim4);}
        var anim4 = function () {
            cloud2.animate({ transform: 't-100 -5'}, 110000, mina.linear, anim3);}
        var anim5 = function () {
            cloud3.animate({ transform: 't-180 50'}, 80000, mina.linear, anim6);}
        var anim6 = function () {
            cloud3.animate({ transform: 't200 -25'}, 80000, mina.linear, anim5);}
        anim1();
        anim3();
        anim5();
    }
    var tabsAnim = async function(){
        var rate = paper.select('#user-friendly-heart-rate');
        var oxygen = paper.select('#user-friendly-oxygen');
        var status = paper.select('#user-friendly-status');
        var beat = paper.select('#user-friendly-heart-beat');
        var tab = paper.select('#user-friendly-tab');
        var animateAlongPath = function( path, element, start, dur ) {
            var len = Snap.path.getTotalLength( path );
            setTimeout( function() {
                   Snap.animate( 0, len, function( value ) {
                   var movePoint = Snap.path.getPointAtLength(path,value);
                   console.log(movePoint);
                   element.transform('t' + movePoint.x + ',' + movePoint.y)	 ;		 
                   }, dur,mina.easeinout); 
            });
        } 
        //var path = rate.path("M 60 0 L 120 0 L 180 60 L 180 120 L 120 180 L 60 180 L 0 120 L 0 60 Z").attr({ fill: "none", stroke: "red", opacity: "1" });
        //todo

        var anim1 = function () {
            rate.animate({ transform: 't130 5'}, 90000, mina.linear, anim2);
        }
        var anim2 = function () {
            rate.animate({ transform: 't-300 -25'}, 90000, mina.linear, anim1);
        }

        //anim1();
    }
    var signAnim = function(){
        var text = paper.select('#scene-sign-text').selectAll('path');
        paper.select('#sign').addClass('pointer').click(function(){window.location = "/register";});

        var signAnim = function(){
            tAnim(text[0],'t0 -10','t0 0',100);
            tAnim(text[1],'t0 -7','t0 3',200);
            tAnim(text[2],'t0 -5','t0 5',300);
            tAnim(text[3],'t0 -4','t0 6',400);
            tAnim(text[4],'t0 -7','t0 3',500);
            tAnim(text[5],'t0 -10','t0 0',600);
            tAnim(text[6],'t0 -10','t0 0',100);
            tAnim(text[7],'t0 -7','t0 3',200);
            tAnim(text[8],'t0 -10','t0 0',300);
        }
        var tAnim = function(el,t1,t2,ts){
            setTimeout(()=>{
                anim1(el,t1,t2);
            },ts);
        }
        var anim1 = function (el,t1,t2) {
            el.animate({transform:t1},1300,mina.easeinout, function(){anim2(el,t1,t2);});
        }
        var anim2 = function (el,t1,t2) {
            el.animate({transform:t2},900,mina.easeinout, function(){anim1(el,t1,t2);});
        }
        signAnim();
        
    }

    heartBeatAnim();
    handAnim();
    cloudsAnim();
    tabsAnim();
    signAnim();
}

genSky();