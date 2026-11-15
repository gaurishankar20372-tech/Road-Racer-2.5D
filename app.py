# ============================================================
# ROAD RACER 2.5D
# Developed by MG Shankar Tech
# Python 3 | Single File | Render Ready
# No API Key | No External Python Packages
# ============================================================

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="theme-color" content="#101923">
<title>ROAD RACER 2.5D</title>

<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#101923;font-family:Arial,sans-serif;color:#fff;touch-action:none}
#game{position:fixed;inset:0;width:100%;height:100%;display:block;background:#24583e}
#hud{position:absolute;top:0;left:0;right:0;min-height:58px;padding:10px 8px;background:rgba(5,12,18,.88);display:flex;align-items:center;justify-content:space-around;gap:4px;z-index:3;font-size:clamp(10px,2.7vw,15px);font-weight:800;white-space:nowrap}
.huditem{padding:7px 5px;border-right:2px solid #78828b}
.huditem:last-child{border:0}
button{border:0;color:white;font-weight:800;cursor:pointer;touch-action:none}
#pause{position:absolute;right:12px;top:75px;z-index:4;background:#263f61;border-radius:18px;padding:17px 22px;font-size:17px}
#controls{position:absolute;bottom:18px;left:0;right:0;display:flex;align-items:center;justify-content:space-around;z-index:4}
.control{width:20vw;max-width:140px;height:76px;border:3px solid #fff;border-radius:22px;background:#294363;font-size:32px;box-shadow:0 4px 0 rgba(0,0,0,.25)}
#brake{width:29vw;max-width:190px;background:#c83d4b;font-size:22px}
#menu,#dialog{position:absolute;inset:0;z-index:10;display:flex;align-items:center;justify-content:center;background:linear-gradient(145deg,rgba(8,17,27,.96),rgba(20,45,59,.96));padding:16px;overflow:auto}
.panel{width:min(720px,100%);max-height:100%;overflow:auto;background:rgba(17,31,45,.97);border:1px solid #49647b;border-radius:24px;padding:20px;box-shadow:0 15px 50px #0009}
h1{font-size:clamp(28px,7vw,48px);margin:0 0 5px;text-align:center;letter-spacing:2px}
.sub{text-align:center;color:#b7c9d7;margin:0 0 18px}
.menuGrid{display:grid;grid-template-columns:1fr 1fr;gap:15px}
.card{background:#20364b;border-radius:17px;padding:14px}
.card h3{margin:0 0 10px;font-size:16px}
#preview{display:block;width:100px;height:145px;margin:auto;background:#26333e;border-radius:12px}
.colors{display:flex;flex-wrap:wrap;gap:9px;justify-content:center}
.colorBtn{width:31px;height:31px;border-radius:50%;border:3px solid #fff5;box-shadow:0 0 0 1px #0008}
.colorBtn.active{outline:3px solid #ffe36a;outline-offset:3px}
#levels{display:grid;grid-template-columns:repeat(5,1fr);gap:7px}
.levelBtn{height:42px;border-radius:10px;background:#2c506c;font-size:14px}
.levelBtn.selected{background:#e6a82d;color:#1b2630;outline:2px solid #fff}
.levelBtn:disabled{background:#29313a;color:#78818a;opacity:.8}
.stats{text-align:center;color:#d5e3ed;line-height:1.7;font-size:14px;margin-top:10px}
.mainBtn{display:block;width:100%;padding:16px;margin-top:14px;border-radius:14px;background:#21a56e;font-size:18px}
.smallBtn{padding:12px 16px;border-radius:12px;background:#365878;margin:7px}
#dialog{background:rgba(4,10,17,.48);z-index:9}
#dialog .panel{text-align:center;background:rgba(15,28,43,.84);backdrop-filter:blur(4px);border:2px solid #ffe17a}
#dialog h2{font-size:clamp(28px,7vw,44px);margin:5px 0 10px;text-shadow:0 0 18px #ffcf45}
#dialog p{font-size:17px}
#dialog button{padding:14px 18px;border-radius:12px;background:#21a56e;margin:6px;font-size:15px}
#dialog .secondary{background:#365878}
.hidden{display:none!important}
@media(max-width:520px){
 .menuGrid{grid-template-columns:1fr}
 #menu{padding:8px}
 .panel{padding:14px}
 #levels{grid-template-columns:repeat(5,1fr)}
}
</style>
</head>

<body>

<canvas id="game"></canvas>

<div id="hud" class="hidden">
 <div class="huditem">SCORE: <span id="score">0</span></div>
 <div class="huditem">COINS: <span id="coins">0</span></div>
 <div class="huditem">TARGET: <span id="target">200</span></div>
 <div class="huditem">LEVEL: <span id="level">1</span></div>
 <div class="huditem">SPEED: <span id="speed">1.0</span>x</div>
</div>

<button id="pause" class="hidden">PAUSE</button>

<div id="controls" class="hidden">
 <button id="left" class="control">◀</button>
 <button id="brake" class="control">BRAKE</button>
 <button id="right" class="control">▶</button>
</div>

<div id="menu">
 <div class="panel">

  <h1>ROAD RACER</h1>
  <p class="sub">2.5D HIGHWAY CHALLENGE</p>

  <div class="menuGrid">

   <div class="card">
    <h3>YOUR CAR • LIVE PREVIEW</h3>
    <canvas id="preview" width="160" height="220"></canvas>
    <div class="stats">Choose your car colour</div>
    <div id="colors" class="colors"></div>
   </div>

   <div class="card">
    <h3>SELECT LEVEL</h3>
    <div id="levels"></div>
    <div class="stats" id="progress">Unlocked: 1 / 20<br>Best score: 0</div>
   </div>

  </div>

  <div class="stats">
   Collect coins, avoid traffic and obstacles.
   <br>Every level requires <b>level × 200 coins</b>.
  </div>

  <button id="play" class="mainBtn">▶ PLAY SELECTED LEVEL</button>

 </div>
</div>

<div id="dialog" class="hidden">
 <div class="panel">
  <h2 id="dialogTitle">LEVEL COMPLETE!</h2>
  <p id="dialogText">Great driving!</p>
  <button id="next">NEXT LEVEL</button>
  <button id="retry" class="secondary">RETRY</button>
  <button id="home" class="secondary">MAIN MENU</button>
 </div>
</div>

<script>
"use strict";

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");

const preview=document.getElementById("preview");
const pctx=preview.getContext("2d");

const $=id=>document.getElementById(id);

const COLORS=[
 ["Blue","#258cff"],
 ["Red","#ef4444"],
 ["Green","#20bd73"],
 ["Yellow","#facc15"],
 ["Orange","#fb923c"],
 ["Purple","#a855f7"],
 ["Pink","#ec4899"],
 ["Black","#252a32"],
 ["White","#e8edf2"],
 ["Cyan","#06b6d4"]
];

const MAX_LEVEL=20;

let selectedColor=localStorage.getItem("rr_color")||"#f5a623";

let selectedLevel=1;

let unlockedLevel=Math.max(
 1,
 Math.min(20,Number(localStorage.getItem("rr_unlock")||1))
);

let bestScore=Number(localStorage.getItem("rr_best")||0);

let W=innerWidth,H=innerHeight,dpr=1,state="MENU";

let lane=1;
let score=0;
let coins=0;
let speed=1;
let roadOffset=0;
let objects=[];
let trees=[];
let last=0;
let spawnTimer=0;
let coinTimer=0;
let braking=false;

let celebration=[];
let confetti=[];
let celebrateClock=0;
let burstClock=0;

const player={
 x:0,
 y:0,
 w:Math.max(42,Math.min(62,W*.115)),
 h:Math.max(88,Math.min(118,H*.105))
};

const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));

const rand=(a,b)=>a+Math.random()*(b-a);

function resize(){

 W=innerWidth;
 H=innerHeight;

 dpr=Math.min(devicePixelRatio||1,2);

 canvas.width=Math.floor(W*dpr);
 canvas.height=Math.floor(H*dpr);

 canvas.style.width=W+"px";
 canvas.style.height=H+"px";

 ctx.setTransform(dpr,0,0,dpr,0,0);

 player.w=clamp(W*.115,43,64);
 player.h=clamp(H*.105,88,120);

 // Player car moved slightly upward
 player.y=H*.69;

 player.x=laneX(lane,player.y)-player.w/2;

 drawPreview();
}

addEventListener("resize",resize);

function targetForLevel(l){
 return l*200;
}

function roadBounds(y){

 let t=clamp(y/H,0,1);

 let half=(W*.34)+(W*.14*t);

 return {
  left:W/2-half,
  right:W/2+half
 };
}

function laneX(n,y){

 let b=roadBounds(y);

 return b.left+(b.right-b.left)*(n+.5)/3;
}

function rounded(c,x,y,w,h,r){

 c.beginPath();

 if(c.roundRect)c.roundRect(x,y,w,h,r);
 else c.rect(x,y,w,h);

 c.fill();
}


// ============================================================
// CAR DRAWING
// FRONT = TOP OF SCREEN
// REAR = BOTTOM OF SCREEN
// ============================================================

function drawCarOn(c,x,y,w,h,color,isPlayer=true,isBraking=false){

 c.save();

 c.shadowColor="#0009";
 c.shadowBlur=8;
 c.shadowOffsetY=5;

 rounded(
  c,
  x+w*.08,
  y+h*.08,
  w*.84,
  h*.84,
  w*.18
 );

 c.shadowBlur=0;
 c.shadowOffsetY=0;

 // Body shell

 let grad=c.createLinearGradient(x,y,x+w,y);

 grad.addColorStop(0,"#333b45");
 grad.addColorStop(.18,color);
 grad.addColorStop(.82,color);
 grad.addColorStop(1,"#343b43");

 c.fillStyle=grad;

 rounded(
  c,
  x+w*.12,
  y+h*.02,
  w*.76,
  h*.96,
  w*.17
 );

 // FRONT BUMPER - TOP

 c.fillStyle="#d9e1e8";

 rounded(
  c,
  x+w*.20,
  y+h*.025,
  w*.60,
  h*.075,
  w*.035
 );

 // FRONT HEADLIGHTS

 c.fillStyle="#fff7c2";

 rounded(c,x+w*.17,y+h*.075,w*.17,h*.055,w*.025);
 rounded(c,x+w*.66,y+h*.075,w*.17,h*.055,w*.025);

 c.fillStyle="#27313b";

 rounded(
  c,
  x+w*.39,
  y+h*.105,
  w*.22,
  h*.045,
  w*.02
 );

 // BONNET

 c.fillStyle=color;

 rounded(
  c,
  x+w*.23,
  y+h*.14,
  w*.54,
  h*.22,
  w*.08
 );

 c.strokeStyle="#fff8";
 c.lineWidth=2;
 c.beginPath();
 c.moveTo(x+w*.42,y+h*.25);
 c.lineTo(x+w*.5,y+h*.18);
 c.lineTo(x+w*.58,y+h*.25);
 c.stroke();

 // FRONT WINDSCREEN

 c.fillStyle="#102b40";

 rounded(
  c,
  x+w*.20,
  y+h*.36,
  w*.60,
  h*.20,
  w*.08
 );

 c.fillStyle="#8bd8ed99";

 c.beginPath();
 c.moveTo(x+w*.25,y+h*.39);
 c.lineTo(x+w*.43,y+h*.39);
 c.lineTo(x+w*.29,y+h*.52);
 c.closePath();
 c.fill();

 // ROOF

 c.fillStyle=color;

 rounded(
  c,
  x+w*.19,
  y+h*.57,
  w*.62,
  h*.20,
  w*.07
 );

 // REAR WINDOW - BOTTOM

 c.fillStyle="#102b40";

 rounded(
  c,
  x+w*.23,
  y+h*.76,
  w*.54,
  h*.105,
  w*.05
 );

 // REAR BUMPER - BOTTOM

 c.fillStyle="#202832";

 rounded(
  c,
  x+w*.18,
  y+h*.89,
  w*.64,
  h*.07,
  w*.025
 );

 // BRAKE LIGHTS

 if(isPlayer && isBraking){

  c.save();

  c.shadowColor="#ff102b";
  c.shadowBlur=24;

  c.fillStyle="#ff102b";

  rounded(
   c,
   x+w*.145,
   y+h*.895,
   w*.22,
   h*.085,
   w*.025
  );

  rounded(
   c,
   x+w*.635,
   y+h*.895,
   w*.22,
   h*.085,
   w*.025
  );

  c.restore();

 }else{

  c.fillStyle="#ff3348";

  rounded(
   c,
   x+w*.16,
   y+h*.91,
   w*.19,
   h*.055,
   w*.025
  );

  rounded(
   c,
   x+w*.65,
   y+h*.91,
   w*.19,
   h*.055,
   w*.025
  );
 }

 // REAR REFLECTOR

 c.fillStyle="#ff7a83";

 rounded(
  c,
  x+w*.38,
  y+h*.925,
  w*.24,
  h*.018,
  w*.008
 );

 // WHEELS

 c.fillStyle="#10151b";

 rounded(c,x+w*.02,y+h*.18,w*.13,h*.22,w*.04);
 rounded(c,x+w*.85,y+h*.18,w*.13,h*.22,w*.04);

 rounded(c,x+w*.02,y+h*.66,w*.13,h*.20,w*.04);
 rounded(c,x+w*.85,y+h*.66,w*.13,h*.20,w*.04);

 c.restore();
}


// ============================================================
// CAR PREVIEW
// ============================================================

function drawPreview(){

 pctx.clearRect(0,0,preview.width,preview.height);

 pctx.fillStyle="#263744";

 pctx.fillRect(
  0,0,
  preview.width,
  preview.height
 );

 drawCarOn(
  pctx,
  48,24,
  64,170,
  selectedColor,
  true,
  false
 );
}


// ============================================================
// MENU
// ============================================================

function renderMenu(){

 $("colors").innerHTML="";

 COLORS.forEach(([name,col])=>{

  let b=document.createElement("button");

  b.className="colorBtn"+
   (selectedColor===col?" active":"");

  b.style.background=col;
  b.title=name;

  b.onclick=()=>{

   selectedColor=col;

   localStorage.setItem("rr_color",col);

   renderMenu();
   drawPreview();
  };

  $("colors").appendChild(b);
 });

 $("levels").innerHTML="";

 for(let i=1;i<=MAX_LEVEL;i++){

  let b=document.createElement("button");

  b.className="levelBtn"+
   (i===selectedLevel?" selected":"");

  b.textContent=i>unlockedLevel?"🔒":i;

  b.disabled=i>unlockedLevel;

  b.onclick=()=>{
   selectedLevel=i;
   renderMenu();
  };

  $("levels").appendChild(b);
 }

 $("progress").innerHTML=
  "Unlocked: "+unlockedLevel+
  " / 20<br>Best score: "+bestScore+
  "<br>Selected target: "+targetForLevel(selectedLevel)+" coins";

 drawPreview();
}


// ============================================================
// GAME CONTROL
// ============================================================

function showGame(){

 $("menu").classList.add("hidden");
 $("hud").classList.remove("hidden");
 $("pause").classList.remove("hidden");
 $("controls").classList.remove("hidden");
 $("dialog").classList.add("hidden");
}

function startGame(level=selectedLevel){

 selectedLevel=level;

 state="PLAY";

 lane=1;
 score=0;
 coins=0;
 speed=1;
 roadOffset=0;

 objects=[];
 trees=[];

 spawnTimer=.7;
 coinTimer=.5;

 braking=false;

 player.y=H*.69;
 player.x=laneX(lane,player.y)-player.w/2;

 $("score").textContent=0;
 $("coins").textContent=0;
 $("target").textContent=targetForLevel(level);
 $("level").textContent=level;
 $("speed").textContent="1.0";

 showGame();

 last=performance.now();
}

function move(dir){

 if(state!=="PLAY")return;

 lane=clamp(lane+dir,0,2);

 player.x=laneX(lane,player.y)-player.w/2;
}

function pauseGame(){

 if(state==="PLAY"){

  state="PAUSE";
  $("pause").textContent="RESUME";
  braking=false;

 }else if(state==="PAUSE"){

  state="PLAY";
  $("pause").textContent="PAUSE";

  last=performance.now();
 }
}

function gameOver(){

 if(state!=="PLAY")return;

 state="OVER";

 bestScore=Math.max(bestScore,score);

 localStorage.setItem("rr_best",bestScore);

 $("dialogTitle").textContent="GAME OVER";

 $("dialogText").textContent=
  "Score: "+score+" • Coins: "+coins;

 $("next").classList.add("hidden");
 $("retry").classList.remove("hidden");

 $("dialog").classList.remove("hidden");
}

function levelComplete(){

 if(state!=="PLAY")return;

 state="COMPLETE";

 unlockedLevel=Math.max(
  unlockedLevel,
  Math.min(MAX_LEVEL,selectedLevel+1)
 );

 localStorage.setItem("rr_unlock",unlockedLevel);

 bestScore=Math.max(bestScore,score);

 localStorage.setItem("rr_best",bestScore);

 $("dialogTitle").textContent=
  selectedLevel===MAX_LEVEL?
  "ALL LEVELS COMPLETE!":
  "LEVEL "+selectedLevel+" COMPLETE!";

 $("dialogText").textContent=
  "Amazing driving! You collected "+coins+" coins.";

 $("next").textContent=
  selectedLevel===MAX_LEVEL?
  "BACK TO MENU":
  "NEXT LEVEL";

 $("next").classList.remove("hidden");
 $("retry").classList.add("hidden");

 $("dialog").classList.remove("hidden");

 startCelebration();
}

function backMenu(){

 state="MENU";

 $("dialog").classList.add("hidden");
 $("hud").classList.add("hidden");
 $("pause").classList.add("hidden");
 $("controls").classList.add("hidden");

 $("menu").classList.remove("hidden");

 renderMenu();
}

$("play").onclick=()=>startGame(selectedLevel);

$("pause").onclick=pauseGame;

$("next").onclick=()=>{
 if(selectedLevel>=MAX_LEVEL)backMenu();
 else startGame(selectedLevel+1);
};

$("retry").onclick=()=>startGame(selectedLevel);

$("home").onclick=backMenu;


// ============================================================
// TOUCH AND KEYBOARD CONTROLS
// ============================================================

$("left").onpointerdown=e=>{
 e.preventDefault();
 move(-1);
};

$("right").onpointerdown=e=>{
 e.preventDefault();
 move(1);
};

$("brake").onpointerdown=e=>{
 e.preventDefault();
 braking=true;
};

["pointerup","pointercancel","pointerleave"].forEach(ev=>{
 $("brake").addEventListener(ev,()=>braking=false);
});

addEventListener("keydown",e=>{

 if(["ArrowLeft","ArrowRight","ArrowDown"," "].includes(e.key)){
  e.preventDefault();
 }

 if(e.key==="ArrowLeft"||e.key.toLowerCase()==="a")move(-1);

 if(e.key==="ArrowRight"||e.key.toLowerCase()==="d")move(1);

 if(e.key===" "||e.key==="ArrowDown")braking=true;

 if(e.key==="Escape")pauseGame();
});

addEventListener("keyup",e=>{

 if(e.key===" "||e.key==="ArrowDown"){
  braking=false;
 }
});

document.addEventListener("visibilitychange",()=>{

 if(document.hidden&&state==="PLAY"){
  pauseGame();
 }
});


// ============================================================
// SPAWN OBJECTS
// ============================================================

function spawnCoin(){

 let ln=Math.floor(Math.random()*3);

 objects.push({
  type:"coin",
  lane:ln,
  y:-35,
  r:Math.max(12,W*.024),
  taken:false
 });
}

function spawnEnemy(){

 let ln=Math.floor(Math.random()*3);

 objects.push({
  type:Math.random()<.18?"block":"car",
  lane:ln,
  y:-130,
  w:player.w*.88,
  h:player.h*.88,
  color:["#e84a4a","#4c9de8","#d6dce4","#a96be8"][
   Math.floor(Math.random()*4)
  ]
 });
}


// ============================================================
// GAME UPDATE
// ============================================================

function update(dt){

 if(state!=="PLAY")return;

 speed=1+selectedLevel*.035+coins*.0004;

 if(braking){
  speed*=.48;
 }

 let flow=H*.55*speed*dt;

 roadOffset=(roadOffset+flow)%90;

 score+=Math.round(flow*.035);

 spawnTimer-=dt;
 coinTimer-=dt;

 if(spawnTimer<=0){

  spawnEnemy();

  spawnTimer=rand(1.0,1.8)/Math.min(2,speed);
 }

 if(coinTimer<=0){

  spawnCoin();

  coinTimer=rand(.35,.7);
 }

 for(let o of objects){

  o.y+=flow*(o.type==="coin"?1.05:1);
 }

 const px=player.x;
 const py=player.y;
 const pw=player.w;
 const ph=player.h;

 for(let o of objects){

  let ox=laneX(o.lane,o.y);

  if(
   o.type==="coin" &&
   !o.taken &&
   Math.abs(ox-(px+pw/2))<pw*.55 &&
   Math.abs(o.y-(py+ph*.45))<ph*.55
  ){

   o.taken=true;

   coins++;
   score+=10;

   $("coins").textContent=coins;
  }

  if(
   o.type!=="coin" &&
   Math.abs(ox-(px+pw/2))<pw*.68 &&
   Math.abs(o.y+o.h*.5-(py+ph*.5))<ph*.72
  ){

   gameOver();
   return;
  }
 }

 objects=objects.filter(o=>
  o.y<H+180 &&
  !(o.type==="coin"&&o.taken)
 );

 $("score").textContent=score;
 $("coins").textContent=coins;
 $("speed").textContent=speed.toFixed(1);

 if(coins>=targetForLevel(selectedLevel)){
  levelComplete();
 }
}


// ============================================================
// ROAD DRAWING
// ============================================================

function drawRoad(){

 ctx.fillStyle="#24583e";
 ctx.fillRect(0,0,W,H);

 // Grass and trees

 for(let y=-100+(roadOffset%180);y<H+100;y+=180){

  ctx.fillStyle="#2d6749";
  ctx.fillRect(0,y,W,90);

  for(let side of [0,1]){

   let x=side?W*.94:W*.06;

   ctx.fillStyle="#174b35";

   ctx.beginPath();
   ctx.arc(x,y+35,9,0,Math.PI*2);
   ctx.fill();

   ctx.fillStyle="#2e9a5d";

   ctx.beginPath();
   ctx.arc(x-3,y+31,7,0,Math.PI*2);
   ctx.fill();
  }
 }

 let top=roadBounds(0);
 let bot=roadBounds(H);

 // Road

 ctx.fillStyle="#303943";

 ctx.beginPath();

 ctx.moveTo(top.left,0);
 ctx.lineTo(top.right,0);
 ctx.lineTo(bot.right,H);
 ctx.lineTo(bot.left,H);

 ctx.closePath();
 ctx.fill();

 // Road edges

 ctx.strokeStyle="#e6e3d5";
 ctx.lineWidth=6;

 ctx.beginPath();

 ctx.moveTo(top.left,0);
 ctx.lineTo(bot.left,H);

 ctx.moveTo(top.right,0);
 ctx.lineTo(bot.right,H);

 ctx.stroke();

 // Lane markings

 ctx.strokeStyle="#f8f8f5";
 ctx.lineWidth=4;

 for(let k=1;k<=2;k++){

  for(let y=-100+(roadOffset%130);y<H+100;y+=130){

   let y2=y+65;

   let x1=
    top.left+(top.right-top.left)*k/3+
    (bot.left-top.left)*k/3*(y/H);

   let x2=
    top.left+(top.right-top.left)*k/3+
    (bot.left-top.left)*k/3*(y2/H);

   ctx.beginPath();
   ctx.moveTo(x1,y);
   ctx.lineTo(x2,y2);
   ctx.stroke();
  }
 }
}


// ============================================================
// COIN DRAWING
// ============================================================

function drawCoin(x,y,r){

 ctx.save();

 ctx.shadowColor="#ffd84d";
 ctx.shadowBlur=15;

 ctx.fillStyle="#ffc928";

 ctx.beginPath();
 ctx.arc(x,y,r,0,Math.PI*2);
 ctx.fill();

 ctx.shadowBlur=0;

 ctx.strokeStyle="#fff2a5";
 ctx.lineWidth=3;
 ctx.stroke();

 ctx.fillStyle="#8b5b00";
 ctx.font="bold "+(r*1.45)+"px Arial";
 ctx.textAlign="center";
 ctx.textBaseline="middle";

 ctx.fillText("$",x,y+1);

 ctx.restore();
}


// ============================================================
// MAIN DRAW
// ============================================================

function draw(){

 drawRoad();

 for(let o of objects){

  let x=laneX(o.lane,o.y);

  if(o.type==="coin"){

   drawCoin(x,o.y,o.r);

  }else if(o.type==="block"){

   ctx.fillStyle="#e9a52c";

   rounded(
    ctx,
    x-player.w*.35,
    o.y,
    player.w*.7,
    player.h*.55,
    8
   );

  }else{

   drawCarOn(
    ctx,
    x-o.w/2,
    o.y,
    o.w,
    o.h,
    o.color,
    false,
    false
   );
  }
 }

 if(state!=="MENU"){

  drawCarOn(
   ctx,
   player.x,
   player.y,
   player.w,
   player.h,
   selectedColor,
   true,
   braking
  );
 }
}


// ============================================================
// LEVEL CELEBRATION
// ============================================================

function startCelebration(){

 celebration=[];
 confetti=[];

 celebrateClock=0;
 burstClock=0;

 for(let i=0;i<150;i++){

  confetti.push({
   x:rand(0,W),
   y:rand(-H,H),
   vx:rand(-80,80),
   vy:rand(50,230),
   rot:rand(0,6),
   vr:rand(-5,5),
   s:rand(4,9),
   col:COLORS[Math.floor(Math.random()*COLORS.length)][1]
  });
 }
}

function burst(){

 let x=rand(W*.12,W*.88);
 let y=rand(H*.12,H*.58);

 let col=COLORS[Math.floor(Math.random()*COLORS.length)][1];

 for(let i=0;i<42;i++){

  let a=Math.PI*2*i/42;
  let v=rand(65,230);

  celebration.push({
   x,y,
   vx:Math.cos(a)*v,
   vy:Math.sin(a)*v,
   life:rand(.8,1.5),
   max:1.5,
   col
  });
 }
}

function updateCelebration(dt){

 celebrateClock+=dt;

 burstClock-=dt;

 if(burstClock<=0&&celebrateClock<7){

  burst();
  burstClock=.35;
 }

 for(let p of celebration){

  p.x+=p.vx*dt;
  p.y+=p.vy*dt;
  p.vy+=110*dt;
  p.life-=dt;
 }

 celebration=celebration.filter(p=>p.life>0);

 for(let f of confetti){

  f.x+=f.vx*dt;
  f.y+=f.vy*dt;
  f.rot+=f.vr*dt;

  if(f.y>H+15){

   f.y=-15;
   f.x=rand(0,W);
  }
 }
}

function drawCelebration(){

 for(let p of celebration){

  ctx.globalAlpha=clamp(p.life/p.max,0,1);

  ctx.fillStyle=p.col;

  ctx.beginPath();
  ctx.arc(p.x,p.y,3.5,0,Math.PI*2);
  ctx.fill();
 }

 ctx.globalAlpha=1;

 for(let f of confetti){

  ctx.save();

  ctx.translate(f.x,f.y);
  ctx.rotate(f.rot);

  ctx.fillStyle=f.col;

  ctx.fillRect(-f.s/2,-f.s/2,f.s,f.s*1.7);

  ctx.restore();
 }

 // Colourful flags

 ctx.lineWidth=2;
 ctx.strokeStyle="#fff";

 ctx.beginPath();
 ctx.moveTo(0,70);
 ctx.quadraticCurveTo(W/2,125,W,70);
 ctx.stroke();

 for(let i=0;i<13;i++){

  let x=i*W/12;
  let y=70+Math.sin(i/12*Math.PI)*55;

  ctx.fillStyle=COLORS[i%COLORS.length][1];

  ctx.beginPath();
  ctx.moveTo(x,y);
  ctx.lineTo(x+W/24,y+20);
  ctx.lineTo(x+W/12,y);
  ctx.closePath();
  ctx.fill();
 }
}


// ============================================================
// GAME LOOP
// ============================================================

function frame(now){

 let dt=Math.min(.04,(now-(last||now))/1000);

 last=now;

 if(state==="PLAY"){

  update(dt);
  draw();

 }else if(state==="PAUSE"){

  draw();

 }else if(state==="COMPLETE"){

  draw();
  updateCelebration(dt);
  drawCelebration();

 }else if(state==="OVER"){

  draw();
 }

 requestAnimationFrame(frame);
}

resize();
renderMenu();
requestAnimationFrame(frame);

</script>
</body>
</html>"""


# ============================================================
# PYTHON WEB SERVER
# ============================================================

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path not in ("/", "/index.html"):
            self.send_error(404, "Not Found")
            return

        body = HTML.encode("utf-8")

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.send_header(
            "Cache-Control",
            "no-store"
        )

        self.end_headers()

        try:
            self.wfile.write(body)
        except BrokenPipeError:
            pass

    def log_message(self, fmt, *args):
        print("[ROAD RACER]", fmt % args)


def main():

    server = ThreadingHTTPServer(
        (HOST, PORT),
        Handler
    )

    print("ROAD RACER is running.")
    print("Local address: http://127.0.0.1:" + str(PORT))
    print("Render Web Service is ready.")

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        server.server_close()


if __name__ == "__main__":
    main()
