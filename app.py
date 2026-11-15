from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 8000

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>ROAD RACER 2.5D</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#101827;color:white;font-family:Arial,sans-serif;overflow:hidden;touch-action:none}
button{border:0;border-radius:12px;padding:12px;font-weight:bold;cursor:pointer}
#menu{position:fixed;inset:0;overflow-y:auto;text-align:center;padding:15px 12px 30px;background:linear-gradient(145deg,#102338,#294b68,#101827)}
.title{font-size:34px;color:#ffda65;margin:15px 0;text-shadow:0 4px 12px #0009}
.panel{background:#ffffff12;border:1px solid #ffffff35;border-radius:18px;padding:15px;margin:12px auto;max-width:520px;box-shadow:0 8px 22px #0004}
.panel h2{color:#9dd6ff;margin:5px 0 12px}
.color-list{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.color{width:40px;height:40px;border-radius:50%;border:3px solid white;padding:0}
.color.selected{outline:4px solid #ffd54f;outline-offset:3px}
.preview-box{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap}
#preview{width:110px;height:155px;border-radius:12px;background:#26394c;border:2px solid #ffffff55}
.level-list{display:grid;grid-template-columns:repeat(4,1fr);gap:9px}
.level-btn{background:#34465c;color:white;padding:14px 4px;font-size:13px}
.level-btn.unlocked{background:#25865b}
.level-btn.selected{background:#ffbd4a;color:#222}
.level-btn:disabled{opacity:.35}
.mainbtn{width:85%;max-width:320px;padding:16px;margin:12px;background:linear-gradient(135deg,#65f0a5,#29b875);color:#10251b;font-size:17px}
.info{background:#ffffff10;padding:9px;margin:7px 0;border-radius:8px;display:flex;justify-content:space-between}
#gameUI{position:fixed;inset:0;display:none}
#game{width:100%;height:100%;display:block}
#hud{position:absolute;top:0;left:0;right:0;padding:12px 5px;background:#0009;display:flex;justify-content:space-around;gap:3px;font-size:11px;font-weight:bold;z-index:2}
#controls{position:absolute;bottom:15px;left:0;right:0;display:grid;grid-template-columns:1fr 1fr 1fr;align-items:center;padding:0 12px;z-index:3}
.ctrl{height:65px;border:2px solid white;background:#263e5c;color:white;font-size:24px;touch-action:none}
#left{justify-self:start;width:75px}
#right{justify-self:end;width:75px}
#brake{justify-self:center;width:105px;background:#c43f45;font-size:16px}
#pause{position:absolute;right:10px;top:62px;z-index:4;background:#263e5c;color:white;padding:9px 13px}
#overlay{position:absolute;inset:0;display:none;align-items:center;justify-content:center;background:#06101b88;z-index:5;overflow:hidden}
.dialog{position:relative;z-index:3;background:linear-gradient(145deg,#203c59,#10243b);padding:24px 18px;width:88%;max-width:370px;border-radius:20px;text-align:center;border:2px solid #ffe16c;box-shadow:0 0 35px #ffdb5c66}
.dialog h1{color:#ffe16c;font-size:25px}
.dialog p{line-height:1.6}
.dialog button{margin:7px;min-width:125px;background:#56d996;color:#10251b}
#nextButton{background:#ffca55}
#celebrationCanvas{position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none}
@media(max-width:380px){.title{font-size:29px}#hud{font-size:9px}.ctrl{height:58px}}
</style>
</head>
<body>

<div id="menu">
<h1 class="title">🏎 ROAD RACER 2.5D</h1>

<div class="panel">
<h2>🚘 CAR CUSTOMIZATION</h2>
<p>Choose Your Car Color</p>
<div class="preview-box">
<canvas id="preview" width="150" height="220"></canvas>
<div><h3 id="selectedColor">Blue</h3><p>LIVE CAR PREVIEW</p><p>Your racing car</p></div>
</div>
<div class="color-list" id="colors"></div>
</div>

<div class="panel">
<h2>🏁 LEVEL SELECTION</h2>
<p id="progress">Unlocked: 1 / 20</p>
<div class="level-list" id="levels"></div>
<p id="levelTarget">Target: 200 Coins</p>
</div>

<div class="panel">
<h2>🎮 GAME INFORMATION</h2>
<div class="info"><span>🏆 Best Score</span><b id="best">0</b></div>
<div class="info"><span>🔓 Unlocked Levels</span><b id="unlockedInfo">1 / 20</b></div>
<p>🪙 Collect coins to complete levels.</p>
<p>🚗 Avoid other vehicles.</p>
<p>⬅ LEFT &nbsp; BRAKE &nbsp; RIGHT ➡</p>
</div>

<button class="mainbtn" onclick="startGame()">▶ PLAY SELECTED LEVEL</button>
</div>

<div id="gameUI">
<canvas id="game"></canvas>
<div id="hud">
<span id="score">SCORE: 0</span>
<span id="coin">COINS: 0</span>
<span id="target">TARGET: 200</span>
<span id="levelHUD">LEVEL: 1</span>
<span id="speed">SPEED: 1x</span>
</div>
<button id="pause" onclick="pauseGame()">PAUSE</button>
<div id="controls">
<button class="ctrl" id="left">◀</button>
<button class="ctrl" id="brake">BRAKE</button>
<button class="ctrl" id="right">▶</button>
</div>
<div id="overlay">
<canvas id="celebrationCanvas"></canvas>
<div class="dialog">
<h1 id="dialogTitle">🎉 LEVEL COMPLETE!</h1>
<p id="dialogText"></p>
<button id="nextButton" onclick="nextLevel()">NEXT LEVEL</button>
<button onclick="backMenu()">MAIN MENU</button>
</div>
</div>
</div>

<script>
"use strict";

const $=id=>document.getElementById(id);
const canvas=$("game"),ctx=canvas.getContext("2d");
const preview=$("preview"),pctx=preview.getContext("2d");
const celebrationCanvas=$("celebrationCanvas"),fctx=celebrationCanvas.getContext("2d");

const MAX_LEVEL=20;

const COLORS=[
 ["Blue","#278cff"],["Red","#ef4444"],["Green","#22c55e"],
 ["Yellow","#facc15"],["Orange","#fb923c"],["Purple","#a855f7"],
 ["Pink","#ec4899"],["Black","#222222"],["White","#eeeeee"],
 ["Cyan","#06b6d4"]
];

const themes=[
 ["#263b50","#315e43","#ffffff"],["#382c25","#80603d","#ffe09a"],
 ["#143c4b","#176477","#67e8f9"],["#32243f","#69427c","#d8b4fe"],
 ["#423321","#80612f","#facc15"],["#183b2c","#286b43","#86efac"],
 ["#34384c","#535d85","#a5b4fc"],["#25364c","#416080","#bae6fd"],
 ["#452a3a","#783d5d","#fbcfe8"],["#263449","#45658c","#93c5fd"],
 ["#44382c","#826b48","#fde68a"],["#193e38","#287263","#99f6e4"],
 ["#392d52","#67518d","#ddd6fe"],["#3b3030","#775050","#fed7aa"],
 ["#492b32","#8b3d4d","#fda4af"],["#1d3b2b","#39754a","#bbf7d0"],
 ["#283d52","#52728f","#bae6fd"],["#333333","#555555","#eeeeee"],
 ["#243e50","#386a80","#a5f3fc"],["#30243d","#644477","#fde68a"]
];

let selectedColor="#278cff",selectedLevel=1,unlockedLevel=1,bestScore=0,currentLevel=1;
let W=innerWidth,H=innerHeight,DPR=1,state="MENU";
let lane=1,score=0,coins=0,speed=1,elapsed=0,roadOffset=0;
let coinTimer=0,enemyTimer=0,brake=false;
let coinList=[],enemies=[],particles=[],celebrationParticles=[];
let carW=45,carH=75,playerY=0;
let last=performance.now(),celebrationTime=0,nextBurst=0;

function targetForLevel(l){return l*200}
function currentTheme(){return themes[Math.min(19,currentLevel-1)]}

function save(){
 try{
  localStorage.setItem("rr_data",JSON.stringify({
   selectedColor,selectedLevel,unlockedLevel,bestScore
  }));
 }catch(e){}
}

function load(){
 try{
  const d=JSON.parse(localStorage.getItem("rr_data")||"{}");
  selectedColor=d.selectedColor||selectedColor;
  unlockedLevel=Math.max(1,Math.min(20,Number(d.unlockedLevel)||1));
  selectedLevel=Math.max(1,Math.min(unlockedLevel,Number(d.selectedLevel)||1));
  bestScore=Number(d.bestScore)||0;
 }catch(e){}
}

load();

function rr(c,x,y,w,h,r){
 c.beginPath();
 if(c.roundRect)c.roundRect(x,y,w,h,r);
 else c.rect(x,y,w,h);
}

/*
 PLAYER CAR:
 कार का फ्रंट स्क्रीन के ऊपर की ओर है।
 ब्रेक लाइट कार के पीछे यानी स्क्रीन के नीचे हैं।
 कार को 180 डिग्री नहीं घुमाया गया है।
*/
function drawCar(c,x,y,w,h,color,isPlayer=false,braking=false){
 c.save();

 // Wheels
 c.fillStyle="#101216";
 const ww=w*.17,wh=h*.23;

 for(const side of [-1,1]){
  for(const pos of [.20,.72]){
   rr(c,x+(side===-1?-ww*.65:w-ww*.35),y+h*pos,ww,wh,4);
   c.fill();
  }
 }

 // Body shadow
 c.fillStyle="#0008";
 rr(c,x+3,y+5,w,h,10);
 c.fill();

 // Body
 let body=c.createLinearGradient(x,y,x+w,y);
 body.addColorStop(0,"#777777");
 body.addColorStop(.18,color);
 body.addColorStop(.75,color);
 body.addColorStop(1,"#111111");

 c.fillStyle=body;
 rr(c,x,y,w,h,Math.max(7,w*.18));
 c.fill();

 c.strokeStyle="#ffffff66";
 c.lineWidth=1.5;
 rr(c,x+2,y+3,w-4,h-6,Math.max(6,w*.15));
 c.stroke();

 // Front bonnet
 c.fillStyle="#ffffff35";
 rr(c,x+w*.13,y+h*.06,w*.74,h*.19,5);
 c.fill();

 c.fillStyle="#151b22";
 rr(c,x+w*.34,y+h*.045,w*.32,h*.055,3);
 c.fill();

 // Front windshield - थोड़ा आगे/ऊपर शिफ्ट किया गया
 c.fillStyle="#102a3d";
 rr(c,x+w*.15,y+h*.25,w*.70,h*.19,5);
 c.fill();

 c.fillStyle="#b8edff66";
 c.beginPath();
 c.moveTo(x+w*.20,y+h*.27);
 c.lineTo(x+w*.48,y+h*.27);
 c.lineTo(x+w*.25,y+h*.41);
 c.lineTo(x+w*.20,y+h*.41);
 c.fill();

 // Middle body
 c.fillStyle=color;
 rr(c,x+w*.16,y+h*.49,w*.68,h*.21,5);
 c.fill();

 // Rear windshield
 c.fillStyle="#142c3c";
 rr(c,x+w*.18,y+h*.73,w*.64,h*.12,4);
 c.fill();

 // Front headlights - कार के आगे
 c.fillStyle="#fff4bb";
 rr(c,x+w*.08,y+h*.015,w*.25,h*.055,3);
 c.fill();

 rr(c,x+w*.67,y+h*.015,w*.25,h*.055,3);
 c.fill();

 // Rear brake lights - कार के पीछे
 if(isPlayer && braking){
  c.save();
  c.shadowColor="#ff0000";
  c.shadowBlur=25;
  c.fillStyle="#ff0000";

  rr(c,x+w*.08,y+h*.925,w*.25,h*.05,3);
  c.fill();

  rr(c,x+w*.67,y+h*.925,w*.25,h*.05,3);
  c.fill();

  c.restore();

  c.fillStyle="#ffaaaa";
  rr(c,x+w*.12,y+h*.935,w*.16,h*.025,2);
  c.fill();

  rr(c,x+w*.71,y+h*.935,w*.16,h*.025,2);
  c.fill();

 }else{
  c.fillStyle="#b90000";

  rr(c,x+w*.08,y+h*.925,w*.25,h*.05,3);
  c.fill();

  rr(c,x+w*.67,y+h*.925,w*.25,h*.05,3);
  c.fill();
 }

 c.restore();
}

function drawPreview(){
 pctx.clearRect(0,0,150,220);
 pctx.fillStyle="#26394c";
 pctx.fillRect(0,0,150,220);

 pctx.strokeStyle="#ffffff35";
 pctx.lineWidth=3;
 pctx.setLineDash([12,10]);

 pctx.beginPath();
 pctx.moveTo(75,0);
 pctx.lineTo(75,220);
 pctx.stroke();

 pctx.setLineDash([]);

 // Preview में भी कार का फ्रंट ऊपर और बैक लाइट नीचे
 drawCar(pctx,47,42,56,125,selectedColor,true,false);
}

function makeColors(){
 $("colors").innerHTML="";

 COLORS.forEach(c=>{
  const b=document.createElement("button");
  b.className="color";
  b.style.background=c[1];
  b.title=c[0];

  if(selectedColor===c[1])b.classList.add("selected");

  b.onclick=()=>{
   selectedColor=c[1];
   save();
   makeColors();
   drawPreview();
  };

  $("colors").appendChild(b);
 });

 const found=COLORS.find(c=>c[1]===selectedColor);
 $("selectedColor").textContent="Selected: "+(found?found[0]:"Custom");

 drawPreview();
}

function makeLevels(){
 $("levels").innerHTML="";

 for(let i=1;i<=MAX_LEVEL;i++){
  const b=document.createElement("button");
  b.className="level-btn";
  b.textContent=i<=unlockedLevel?"LEVEL "+i:"🔒 "+i;

  if(i<=unlockedLevel)b.classList.add("unlocked");
  if(i===selectedLevel)b.classList.add("selected");

  b.disabled=i>unlockedLevel;

  b.onclick=()=>{
   selectedLevel=i;
   save();
   makeLevels();
  };

  $("levels").appendChild(b);
 }

 $("progress").textContent="Unlocked: "+unlockedLevel+" / "+MAX_LEVEL;
 $("best").textContent=bestScore;
 $("unlockedInfo").textContent=unlockedLevel+" / "+MAX_LEVEL;
 $("levelTarget").textContent="Target: "+targetForLevel(selectedLevel)+" Coins";
}

makeColors();
makeLevels();

function resize(){
 DPR=Math.min(devicePixelRatio||1,2);
 W=innerWidth;
 H=innerHeight;

 canvas.width=W*DPR;
 canvas.height=H*DPR;
 canvas.style.width=W+"px";
 canvas.style.height=H+"px";

 ctx.setTransform(DPR,0,0,DPR,0,0);

 carW=Math.min(W/7,57);
 carH=carW*1.65;

 // खिलाड़ी की कार को थोड़ा आगे/ऊपर रखा गया
 playerY=H-carH-125;

 celebrationCanvas.width=W*DPR;
 celebrationCanvas.height=H*DPR;
 celebrationCanvas.style.width=W+"px";
 celebrationCanvas.style.height=H+"px";

 fctx.setTransform(DPR,0,0,DPR,0,0);
}

addEventListener("resize",resize);
resize();

function roadBounds(y){
 const p=Math.max(0,Math.min(1,y/H));
 const topWidth=W*.70;
 const bottomWidth=W*.96;
 const width=topWidth+(bottomWidth-topWidth)*p;

 return{
  left:(W-width)/2,
  right:(W+width)/2,
  width
 };
}

function laneX(n,y){
 const r=roadBounds(y);
 return r.left+r.width*(n+.5)/3;
}

function drawTree(x,y,size){
 ctx.save();

 ctx.fillStyle="#563b27";
 ctx.fillRect(x-size*.13,y,size*.26,size*.85);

 ctx.fillStyle="#10472d";
 ctx.beginPath();
 ctx.arc(x,y,size*.55,0,Math.PI*2);
 ctx.fill();

 ctx.fillStyle="#287c43";
 ctx.beginPath();
 ctx.arc(x-size*.2,y-size*.18,size*.36,0,Math.PI*2);
 ctx.fill();

 ctx.fillStyle="#4b9d54";
 ctx.beginPath();
 ctx.arc(x+size*.12,y-size*.25,size*.23,0,Math.PI*2);
 ctx.fill();

 ctx.restore();
}

function drawScenery(){
 for(let y=-80+(roadOffset%170);y<H+100;y+=170){
  const b=roadBounds(y);
  const p=Math.max(.2,Math.min(1,y/H));
  const size=7+p*12;

  drawTree(b.left-size*2.4,y,size);
  drawTree(b.right+size*2.4,y+55,size);
 }
}

function drawRoad(){
 const t=currentTheme();

 ctx.fillStyle=t[1];
 ctx.fillRect(0,0,W,H);

 for(let y=-90+(roadOffset%150);y<H+100;y+=150){
  const b=roadBounds(y);
  ctx.fillStyle="#ffffff0a";
  ctx.fillRect(0,y,b.left,3);
  ctx.fillRect(b.right,y,W-b.right,3);
 }

 const top=roadBounds(0);
 const bottom=roadBounds(H);

 ctx.beginPath();
 ctx.moveTo(top.left,0);
 ctx.lineTo(top.right,0);
 ctx.lineTo(bottom.right,H);
 ctx.lineTo(bottom.left,H);
 ctx.closePath();

 const g=ctx.createLinearGradient(0,0,0,H);
 g.addColorStop(0,"#353d48");
 g.addColorStop(1,"#252b34");

 ctx.fillStyle=g;
 ctx.fill();

 ctx.strokeStyle="#e7e4d9";
 ctx.lineWidth=5;

 ctx.beginPath();
 ctx.moveTo(top.left,0);
 ctx.lineTo(bottom.left,H);
 ctx.moveTo(top.right,0);
 ctx.lineTo(bottom.right,H);
 ctx.stroke();

 for(let i=1;i<3;i++){
  ctx.strokeStyle=t[2];
  ctx.lineWidth=3;
  ctx.setLineDash([27,24]);
  ctx.lineDashOffset=-roadOffset*.7;

  ctx.beginPath();
  ctx.moveTo(top.left+top.width*i/3,0);
  ctx.lineTo(bottom.left+bottom.width*i/3,H);
  ctx.stroke();
 }

 ctx.setLineDash([]);

 for(let y=-70+(roadOffset%110);y<H+100;y+=110){
  const b=roadBounds(y);
  const p=Math.max(.1,y/H);
  const size=3+4*p;

  ctx.fillStyle="#f5f5f5";
  ctx.fillRect(b.left-size*2,y,size,28*p+10);
  ctx.fillRect(b.right+size,y,size,28*p+10);
 }

 drawScenery();
}

function drawCoin(c){
 ctx.save();
 ctx.translate(c.x,c.y);
 ctx.scale(.65+Math.abs(Math.cos(c.spin))*.35,1);
 ctx.shadowColor="#ffcf33";
 ctx.shadowBlur=13;

 const g=ctx.createRadialGradient(-3,-4,2,0,0,14);
 g.addColorStop(0,"#fff5a8");
 g.addColorStop(.45,"#ffcf32");
 g.addColorStop(1,"#bd7600");

 ctx.fillStyle=g;
 ctx.beginPath();
 ctx.arc(0,0,12,0,Math.PI*2);
 ctx.fill();

 ctx.shadowBlur=0;
 ctx.strokeStyle="#fff1a5";
 ctx.lineWidth=2;
 ctx.stroke();

 ctx.fillStyle="#946000";
 ctx.font="bold 13px Arial";
 ctx.textAlign="center";
 ctx.fillText("$",0,5);

 ctx.restore();
}

function spawnCoins(){
 const base=Math.floor(Math.random()*3);
 const count=4+Math.floor(Math.random()*3);

 for(let i=0;i<count;i++){
  const y=-20-i*42;
  coinList.push({
   lane:base,
   x:laneX(base,y),
   y,
   spin:Math.random()*6
  });
 }
}

function spawnEnemy(){
 const available=[0,1,2].filter(n=>
  !enemies.some(e=>e.lane===n&&e.y<carH*2.5)
 );

 if(!available.length)return;

 const ln=available[Math.floor(Math.random()*available.length)];

 const colors=[
  "#e85b5b","#f59e0b","#a78bfa",
  "#ec4899","#e7edf4","#20b99b"
 ];

 const y=-carH-20;

 enemies.push({
  lane:ln,
  y,
  w:carW*.92,
  h:carH,
  speed:95+currentLevel*5+Math.random()*35,
  color:colors[Math.floor(Math.random()*colors.length)]
 });
}

function startGame(){
 currentLevel=selectedLevel;

 score=0;
 coins=0;
 elapsed=0;
 speed=1;
 lane=1;
 roadOffset=0;

 coinTimer=0;
 enemyTimer=0;

 coinList=[];
 enemies=[];
 particles=[];
 celebrationParticles=[];

 brake=false;
 state="PLAY";

 $("menu").style.display="none";
 $("gameUI").style.display="block";
 $("overlay").style.display="none";
 $("pause").textContent="PAUSE";

 last=performance.now();
}

function move(d){
 if(state==="PLAY"){
  lane=Math.max(0,Math.min(2,lane+d));
 }
}

function bind(id,fn){
 const b=$(id);

 b.addEventListener("pointerdown",e=>{
  e.preventDefault();
  b.setPointerCapture(e.pointerId);
  fn(true);
 });

 ["pointerup","pointercancel","lostpointercapture"].forEach(ev=>
  b.addEventListener(ev,()=>fn(false))
 );
}

bind("left",v=>{if(v)move(-1)});
bind("right",v=>{if(v)move(1)});
bind("brake",v=>{brake=v});

addEventListener("keydown",e=>{
 if(e.key==="ArrowLeft"||e.key==="a")move(-1);
 if(e.key==="ArrowRight"||e.key==="d")move(1);

 if(e.key==="ArrowDown"||e.key===" ")brake=true;

 if(e.key==="Escape")pauseGame();
});

addEventListener("keyup",e=>{
 if(e.key==="ArrowDown"||e.key===" ")brake=false;
});

function pauseGame(){
 if(state==="PLAY"){
  state="PAUSE";
  brake=false;
  $("pause").textContent="RESUME";
 }
 else if(state==="PAUSE"){
  state="PLAY";
  $("pause").textContent="PAUSE";
  last=performance.now();
 }
}

function showDialog(title,message,next){
 $("overlay").style.display="flex";
 $("dialogTitle").textContent=title;
 $("dialogText").textContent=message;
 $("nextButton").style.display=next?"inline-block":"none";
}

function levelComplete(){
 if(state!=="PLAY")return;

 state="COMPLETE";

 if(currentLevel>=unlockedLevel&&unlockedLevel<MAX_LEVEL){
  unlockedLevel=currentLevel+1;
 }

 if(score>bestScore)bestScore=score;

 save();
 makeLevels();

 showDialog(
  currentLevel===MAX_LEVEL?"🏆 CHAMPION!":"🎉 LEVEL "+currentLevel+" COMPLETE!",
  "Amazing! You collected "+coins+" coins! Target: "+targetForLevel(currentLevel)+". Congratulations, Racer!",
  currentLevel<MAX_LEVEL
 );

 startCelebration();
}

function nextLevel(){
 if(currentLevel>=MAX_LEVEL){
  backMenu();
  return;
 }

 selectedLevel=currentLevel+1;
 save();
 makeLevels();
 startGame();
}

function gameOver(){
 if(state!=="PLAY")return;

 state="OVER";

 if(score>bestScore){
  bestScore=score;
  save();
  makeLevels();
 }

 showDialog(
  "GAME OVER",
  "Level: "+currentLevel+" | Coins: "+coins+" / "+targetForLevel(currentLevel)+" | Score: "+score,
  false
 );
}

function backMenu(){
 state="MENU";
 $("gameUI").style.display="none";
 $("menu").style.display="block";
 brake=false;
 makeLevels();
 makeColors();
}

function addParticles(x,y,color,count){
 for(let i=0;i<count;i++){
  const a=Math.random()*Math.PI*2;
  const v=45+Math.random()*190;

  particles.push({
   x,y,
   vx:Math.cos(a)*v,
   vy:Math.sin(a)*v,
   life:.8+Math.random()*.9,
   size:2+Math.random()*3,
   color
  });
 }
}

const partyColors=[
 "#ff3158","#ffe45e","#54e8ff",
 "#a77bff","#5dff9a","#ffffff",
 "#ff8c42","#ff65d4"
];

function createBurst(x,y,color,count){
 for(let i=0;i<count;i++){
  const a=Math.random()*Math.PI*2;
  const v=60+Math.random()*230;

  particles.push({
   x,y,
   vx:Math.cos(a)*v,
   vy:Math.sin(a)*v,
   life:1.1+Math.random()*1.3,
   size:2+Math.random()*3,
   color
  });
 }
}

function startCelebration(){
 particles=[];
 celebrationParticles=[];
 celebrationTime=0;
 nextBurst=0;

 for(let i=0;i<12;i++){
  createBurst(
   W*(.08+Math.random()*.84),
   H*(.08+Math.random()*.55),
   partyColors[i%partyColors.length],
   65
  );
 }

 for(let i=0;i<160;i++){
  celebrationParticles.push({
   x:Math.random()*W,
   y:Math.random()*H,
   vx:(Math.random()-.5)*100,
   vy:40+Math.random()*170,
   size:4+Math.random()*7,
   rotation:Math.random()*6,
   spin:(Math.random()-.5)*7,
   life:4+Math.random()*4,
   color:partyColors[Math.floor(Math.random()*partyColors.length)],
   type:Math.random()>.5?"rect":"ribbon"
  });
 }
}

function updateCelebration(dt){
 celebrationTime+=dt;
 nextBurst-=dt;

 if(nextBurst<=0&&celebrationTime<7){
  createBurst(
   W*(.08+Math.random()*.84),
   H*(.08+Math.random()*.52),
   partyColors[Math.floor(Math.random()*partyColors.length)],
   75
  );

  nextBurst=.30+Math.random()*.35;
 }

 for(let i=particles.length-1;i>=0;i--){
  const p=particles[i];

  p.x+=p.vx*dt;
  p.y+=p.vy*dt;
  p.vx*=.985;
  p.vy*=.985;
  p.vy+=45*dt;
  p.life-=dt;

  if(p.life<=0)particles.splice(i,1);
 }

 for(const p of celebrationParticles){
  p.x+=p.vx*dt;
  p.y+=p.vy*dt;
  p.rotation+=p.spin*dt;
  p.vy+=12*dt;

  if(p.y>H+30)p.y=-20;
 }
}

function drawCelebration(){
 fctx.clearRect(0,0,W,H);

 for(const p of particles){
  fctx.globalAlpha=Math.max(0,Math.min(1,p.life/.45));
  fctx.fillStyle=p.color;
  fctx.shadowColor=p.color;
  fctx.shadowBlur=14;

  fctx.beginPath();
  fctx.arc(p.x,p.y,p.size,0,Math.PI*2);
  fctx.fill();
 }

 fctx.shadowBlur=0;

 for(const p of celebrationParticles){
  fctx.save();
  fctx.translate(p.x,p.y);
  fctx.rotate(p.rotation);

  fctx.globalAlpha=.9;
  fctx.fillStyle=p.color;

  if(p.type==="rect"){
   fctx.fillRect(-p.size/2,-p.size/2,p.size,p.size*.65);
  }else{
   fctx.fillRect(-p.size/2,-p.size*1.5,p.size,p.size*3);
  }

  fctx.restore();
 }

 // Celebration flags
 fctx.save();

 fctx.strokeStyle="#fff4b0";
 fctx.lineWidth=2;

 fctx.beginPath();
 fctx.moveTo(10,35);
 fctx.quadraticCurveTo(W/2,100,W-10,35);
 fctx.stroke();

 const flagColors=[
  "#ff3158","#ffe45e","#54e8ff",
  "#5dff9a","#a77bff"
 ];

 for(let i=0;i<9;i++){
  const x=15+(W-30)*i/8;
  const y=35+Math.sin(i/8*Math.PI)*32;

  fctx.fillStyle=flagColors[i%flagColors.length];

  fctx.beginPath();
  fctx.moveTo(x-8,y);
  fctx.lineTo(x+8,y);
  fctx.lineTo(x,y+22);
  fctx.closePath();
  fctx.fill();
 }

 fctx.restore();

 fctx.globalAlpha=1;

 fctx.save();
 fctx.textAlign="center";
 fctx.font="bold 25px Arial";
 fctx.fillStyle="#ffe45e";
 fctx.shadowColor="#ffbd36";
 fctx.shadowBlur=20;
 fctx.fillText("🏆 LEVEL COMPLETED! 🏆",W/2,H*.13);
 fctx.restore();
}

function update(dt){
 if(state!=="PLAY")return;

 elapsed+=dt;

 speed=Math.min(3.8,1+elapsed*.025);

 if(brake){
  speed=Math.max(.65,speed-2.5*dt);
 }else{
  speed=Math.min(3.8,speed+1.2*dt);
 }

 const travel=speed*230;

 roadOffset=(roadOffset+travel*dt)%180;

 coinTimer+=dt;

 if(coinTimer>.48){
  coinTimer=0;
  spawnCoins();
 }

 enemyTimer+=dt;

 const gap=Math.max(1.0,1.9-currentLevel*.025);

 if(enemyTimer>gap){
  enemyTimer=0;
  spawnEnemy();
 }

 for(const c of coinList){
  c.y+=travel*dt;
  c.x=laneX(c.lane,c.y);
  c.spin+=dt*7;
 }

 const playerX=laneX(lane,playerY);
 const playerCenterY=playerY+carH*.5;

 for(let i=coinList.length-1;i>=0;i--){
  const c=coinList[i];

  if(c.y>H+30){
   coinList.splice(i,1);
   continue;
  }

  const coinX=laneX(c.lane,c.y);
  const closeX=Math.abs(coinX-playerX)<carW*.52;
  const closeY=Math.abs(c.y-playerCenterY)<carH*.55;

  if(closeX&&closeY){
   coins++;
   score+=50;

   addParticles(playerX,playerCenterY,"#ffdf4d",8);

   coinList.splice(i,1);

   if(coins>=targetForLevel(currentLevel)){
    levelComplete();
    return;
   }
  }
 }

 for(let i=enemies.length-1;i>=0;i--){
  const e=enemies[i];

  e.y+=(travel+e.speed)*dt;

  if(e.y>H+80){
   enemies.splice(i,1);
   score+=10;
   continue;
  }

  const enemyX=laneX(e.lane,e.y);

  const overlapX=
   playerX+carW*.34>enemyX-e.w*.34&&
   playerX-carW*.34<enemyX+e.w*.34;

  const overlapY=
   e.y+e.h*.78>playerY+carH*.12&&
   e.y+e.h*.12<playerY+carH*.88;

  if(overlapX&&overlapY){
   gameOver();
   return;
  }
 }

 if(score>bestScore){
  bestScore=score;
  save();
 }
}

function draw(){
 drawRoad();

 coinList.forEach(drawCoin);

 for(const e of enemies){
  const x=laneX(e.lane,e.y);

  drawCar(
   ctx,x-e.w/2,e.y,e.w,e.h,e.color,false,false
  );
 }

 const px=laneX(lane,playerY);

 // Player car: front faces forward, rear brake lights stay at bottom.
 drawCar(
  ctx,
  px-carW/2,
  playerY,
  carW,
  carH,
  selectedColor,
  true,
  brake
 );

 $("score").textContent="SCORE: "+score;
 $("coin").textContent="COINS: "+coins;
 $("target").textContent="TARGET: "+targetForLevel(currentLevel);
 $("levelHUD").textContent="LEVEL: "+currentLevel;
 $("speed").textContent="SPEED: "+speed.toFixed(1)+"x";
}

function frame(now){
 const dt=Math.min(.04,(now-last)/1000||0);
 last=now;

 if(state==="PLAY"){
  update(dt);
  draw();
 }
 else if(state==="PAUSE"){
  draw();
 }
 else if(state==="COMPLETE"){
  drawRoad();
  updateCelebration(dt);
  drawCelebration();
 }
 else if(state==="OVER"){
  draw();
 }

 requestAnimationFrame(frame);
}

requestAnimationFrame(frame);

document.addEventListener("visibilitychange",()=>{
 if(document.hidden&&state==="PLAY"){
  pauseGame();
 }
});
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return

        body = HTML.encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        try:
            self.wfile.write(body)
        except BrokenPipeError:
            pass

    def log_message(self, fmt, *args):
        print("[SERVER]", fmt % args)


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)

    print("=" * 45)
    print("ROAD RACER 2.5D SERVER STARTED")
    print("Open: http://127.0.0.1:8000")
    print("Stop: CTRL + C")
    print("=" * 45)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
