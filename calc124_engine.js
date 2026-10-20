/* 미적분Ⅰ 124쪽 엔진: 그리기 · 형광 연동 · 보기 · 변형 */
const cv=$("#cv"),ctx=cv.getContext("2d");
let cur=0,mi=0,K={},P={},showSol=false,dragged=false,solved={},lockHL=null,hoverHL=null,frozen=null,drag=null,CH=[],cw=600,chh=420,V=null;
window.HLK=[];window.PILLS=[];
const def=()=>PR[cur],mode=()=>def().modes[mi];
const UNK={"1:2":1,"3:3":1,"4:0":1,"4:2":1,"4:3":1,"5:0":1};
const unk=()=>UNK[cur+":"+mi]&&!showSol;
const COL={pos:"#22d3ee",neg:"#fb923c",S:"#4ade80",f:"#f472b6",axis:"#facc15",lo:"#facc15",hi:"#facc15"};
function recomputeHL(){window.HLK=hoverHL||lockHL||[];document.querySelectorAll("[data-hl]").forEach(e=>{const ks=e.dataset.hl.split(",");e.classList.toggle("hkon",window.HLK.length>0&&ks.every(k=>window.HLK.includes(k)))})}
document.addEventListener("mouseover",e=>{const t=e.target.closest&&e.target.closest("[data-hl]");if(t){hoverHL=t.dataset.hl.split(",");recomputeHL()}});
document.addEventListener("mouseout",e=>{const t=e.target.closest&&e.target.closest("[data-hl]");if(t){hoverHL=null;recomputeHL()}});
document.addEventListener("click",e=>{const t=e.target.closest&&e.target.closest("[data-hl]");if(t){const ks=t.dataset.hl.split(",");lockHL=(lockHL&&lockHL.join()===ks.join())?null:ks;recomputeHL()}});

/* ---------- 교과서식 수식 (분수 · 정적분 · 대괄호 구간) ---------- */
const SUBS="₀₁₂₃₄₅₆₇₈₉₋",SUBD={"₀":"0","₁":"1","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9","₋":"−"};
const subTxt=s=>s.replace(/[₀-₉₋]/g,c=>SUBD[c]);
const LOW="(?:[₀-₉₋]+|_\\{[^}]*\\}|_[^\\s^{])",UPP="(?:\\^\\{[^}]*\\}|\\^[^\\s()\\[\\]{}]+|[ˣⁿ])";
const cl=s=>s.replace(/^_/,"").replace(/^\{|\}$/g,"").replace(/^\^/,"").replace(/^\{|\}$/g,"");
const lowT=s=>subTxt(cl(s)),uppT=s=>cl(s);
function fmtSeg(t){
 t=t.replace(new RegExp("∫("+LOW+")("+UPP+")","g"),(m,a,b)=>`<span class="ig"><span class="ign">∫</span><span class="lim"><sup>${uppT(b)}</sup><sub>${lowT(a)}</sub></span></span>`);
 t=t.replace(new RegExp("\\]("+LOW+")("+UPP+")","g"),(m,a,b)=>`<span class="br">]</span><span class="lim"><sup>${uppT(b)}</sup><sub>${lowT(a)}</sub></span>`);
 const par="\\((?:[^()]|\\([^()]*\\))*\\)";
 t=t.replace(new RegExp("(\\d+(?:\\.\\d+)?|"+par+"[²³⁴]?|[A-Za-zα-ωπ]+[²³⁴]?)/(\\d+|[A-Za-z]+[²³⁴]?)","g"),(m,a,b)=>{const n=/^\(/.test(a)&&!/[²³⁴]$/.test(a)?a.slice(1,-1):a;return `<span class="fr"><span>${n}</span><span>${b}</span></span>`});
 return t}
const fmt=h=>String(h).split(/(<[^>]+>)/).map(s=>s[0]==="<"?s:fmtSeg(s)).join("");

/* ---------- 상태 ---------- */
function setMode(i,Kn){mi=i;const m=mode();K=Object.assign({},Kn||m.K);P=def().P(K);dragged=false;showSol=false;frozen=null;lockHL=null;hoverHL=null;mkChoices();render()}
function mkChoices(){const d=def(),m=mode(),a=m.ans(K).fr;
 if(mi===0&&d.bookChoices){CH=d.bookChoices.map((t,i)=>({t,ok:i===d.bookIdx}));return}
 const traps=[];try{const e=exact(d,d.P(K));[e.signed,e.pos,e.neg,e.tot].forEach(v=>traps.push(v))}catch(_){}
 const alt=[a.add(fr(1,a.d)),a.sub(fr(1,a.d)),a.add(fr(1,2)),a.sub(fr(1,2)),a.mul(fr(2)),a.div(fr(2)),a.add(fr(1)),a.sub(fr(1)),a.add(fr(1,3)),a.sub(fr(1,3)),a.add(fr(2)),a.sub(fr(2)),a.mul(fr(3)),a.add(fr(1,6))];
 const seen=new Set([a.str()]),pool=[];const okv=v=>v.str()!==a.str()&&!seen.has(v.str())&&(a.n>0?v.n>0:true)&&(seen.add(v.str()),true);
 traps.forEach(v=>{if(pool.length<2&&okv(v))pool.push(v)});
 alt.sort((x,y)=>Math.abs(x.val()-a.val())-Math.abs(y.val()-a.val()));alt.forEach(v=>{if(pool.length<4&&okv(v))pool.push(v)});
 const all=[{t:a.str(),ok:true,v:a.val()},...pool.map(v=>({t:v.str(),ok:false,v:v.val()}))].sort((x,y)=>x.v-y.v);CH=all}
function renderChoices(){const box=$("#choices");box.innerHTML="";CH.forEach((c,i)=>{const b=document.createElement("button");b.className="ch";b.innerHTML="①②③④⑤"[i]+" "+fmt(c.t);b.onclick=()=>{if(c.ok){b.classList.add("good");solved[cur]=1;renderNav();$("#vmsg").textContent="정답이에요! 풀이 보기로 과정을 확인해 보세요."}else{b.classList.add("bad");$("#vmsg").textContent="다시 생각해 보세요. 부호가 바뀌는 곳을 먼저 찾아요."}};box.appendChild(b)})}
function renderNav(){$("#nav").innerHTML="";PR.forEach((p,i)=>{const b=document.createElement("button");b.className="tb"+(i===cur?" on":"")+(solved[i]?" ok":"");b.textContent=(solved[i]?"✔ ":"")+p.id+(p.tag?" · "+p.tag:"");b.onclick=()=>{cur=i;setMode(0)};$("#nav").appendChild(b)})}
function renderVar(){const d=def(),box=$("#vchips");box.innerHTML="";d.modes.forEach((m,i)=>{const b=document.createElement("button");b.className="vc"+(i===mi?" on":"");b.innerHTML=fmt(m.n);b.title=m.d||"";b.onclick=()=>setMode(i);b.onmouseenter=()=>{hoverHL=m.hl;recomputeHL()};b.onmouseleave=()=>{hoverHL=null;recomputeHL()};box.appendChild(b)});
 const kb=$("#vknobs");kb.innerHTML="";Object.keys(mode().K).filter(k=>k!=="orig").forEach(k=>{const l=document.createElement("label");l.className="cv";l.innerHTML=`${d.L[k]||k}<input type="number" step="1" data-k="${k}" value="${K[k]}">`;kb.appendChild(l)});
 $("#vmsg").textContent=mode().d||"조건을 바꾼 응용 문제예요."}
function readKnobs(){const o={};document.querySelectorAll("#vknobs input").forEach(i=>o[i.dataset.k]=Number(i.value));return o}
function makeVariant(){const d=def(),m=mode(),keys=Object.keys(m.K).filter(k=>k!=="orig");
 if(!keys.length){$("#vmsg").textContent="이 문제는 조건이 숫자 α, β 를 정해 주어서 숫자를 바꿀 수 없어요. 위의 다른 변형 칩을 골라 보세요.";return}
 const mk=Object.assign({},m.K,readKnobs());const valid=k=>d.ok(k)&&(!m.ok||m.ok(k));
 const same=keys.every(k=>mk[k]===K[k]);let Kn=null;
 if(!same){if(valid(mk))Kn=mk;else{$("#vmsg").textContent="그 숫자로는 도형이 만들어지지 않아요. 범위를 확인해 주세요.";return}}
 else{for(let t=0;t<400&&!Kn;t++){const c=Object.assign({},m.K);keys.forEach(k=>{c[k]=m.K[k]+Math.floor(Math.random()*7)-3});if(valid(c)&&keys.some(k=>c[k]!==K[k]))Kn=c}}
 if(!Kn){$("#vmsg").textContent="새 숫자를 만들지 못했어요. 숫자를 직접 입력해 보세요.";return}
 setMode(mi,Kn);$("#vmsg").textContent="새 숫자로 변형 문제를 만들었어요. (숫자를 직접 고쳐도 돼요)"}
function render(){const d=def(),m=mode();$("#qid").innerHTML=`${d.id} · ${m.n}`+(d.tag?`<span class="tag">${d.tag}</span>`:"");$("#q").innerHTML=fmt(m.text(K));$("#solcard").style.display="none";$("#alt").style.display="none";$("#bAlt").textContent="다른 풀이";$("#bSol").textContent="풀이 보기";
 renderChoices();renderNav();renderVar();$("#chint").innerHTML="노란 점을 끌어 보세요. 글씨나 그림 위의 <b>S₁ S₂ S</b> 이름표를 누르면 서로 반응해요.";recomputeHL();sizeCv()}
function solText(){const m=mode(),a=m.ans(K).fr;return m.sol(K).map((l,i)=>`<div style="margin:4px 0">${"①②③④"[i]||"•"} ${fmt(l)}</div>`).join("")+`<div class="big ok" style="margin-top:6px">정답: ${fmt(a.str())}</div>`}
$("#bSol").onclick=()=>{showSol=!showSol;$("#solcard").style.display=showSol?"block":"none";$("#bSol").textContent=showSol?"풀이 접기":"풀이 보기";if(showSol)$("#sol").innerHTML=solText()};
$("#bReset").onclick=()=>{P=def().P(K);dragged=false;frozen=null;lockHL=null;recomputeHL()};
$("#bVar").onclick=makeVariant;$("#bVarOrig").onclick=()=>setMode(0);

/* ---------- 개념 카드 ---------- */
const ico=(up,col)=>`<svg width="52" height="30" viewBox="0 0 52 30"><line x1="2" y1="15" x2="50" y2="15" stroke="#8ea0bb" stroke-width="1.5"/><path d="M6 15 Q26 ${up?-3:33} 46 15 Z" fill="${col}33" stroke="${col}" stroke-width="2"/></svg>`;
const term=(k,cls,sym,cap,svg)=>`<div class="cp-term ${cls}" data-hl="${k}">${svg}<b>${sym}</b><small>${cap}</small></div>`;
$("#concept").innerHTML=`<div class="cp-eq">${term("S","t3","S","전체 넓이",`<svg width="52" height="30" viewBox="0 0 52 30"><line x1="2" y1="15" x2="50" y2="15" stroke="#8ea0bb" stroke-width="1.5"/><path d="M6 15 Q16 0 26 15 Q36 30 46 15 Z" fill="#4ade8033" stroke="#4ade80" stroke-width="2"/></svg>`)}<span class="op">=</span>${term("pos","t1","S₁","x축 위쪽",ico(true,"#22d3ee"))}<span class="op">+</span>${term("neg","t2","S₂","x축 아래쪽",ico(false,"#fb923c"))}</div>
<div class="cp-row"><span class="lab">넓이 공식</span><span>S = ∫ |f(x)| dx  (부호가 바뀌는 점에서 나눈다)</span></div>
<div class="cp-row"><span class="lab">부호 나누기</span><span class="cp-var t1" data-hl="pos">f ≥ 0 → ∫ f dx</span><span class="cp-var t2" data-hl="neg">f ≤ 0 → −∫ f dx</span></div>
<div class="cp-row"><span class="lab">왜 필요할까</span><span>∫ f dx 는 위(+)와 아래(−)가 <b>서로 지워지지만</b>, 넓이는 지우지 않고 더한다 → <span class="cp-tag" data-hl="pos,neg">위·아래를 따로 계산</span></span></div>
<div class="cp-row"><span class="lab">풀이 순서</span><span class="cp-tag" data-hl="axis">① f(x)=0 인 점</span><span class="cp-tag" data-hl="lo,hi">② 구간 끝</span><span class="cp-tag" data-hl="pos,neg">③ 부호별 적분</span><span class="cp-tag" data-hl="S">④ 더하기</span></div>
<div class="cp-row"><span class="lab">출제 단서</span><span class="cp-tag" data-hl="f">곡선 y = f(x)</span><span class="cp-tag" data-hl="axis">x축</span><span class="cp-tag" data-hl="lo,hi">두 직선 · 구간</span><span class="cp-tag" data-hl="S">넓이</span></div>`;

/* ---------- 그리기 ---------- */
function sizeCv(){const dpr=window.devicePixelRatio||1;cw=Math.max(300,cv.clientWidth||600);chh=Math.round(cw*.7);cv.width=cw*dpr;cv.height=chh*dpr;cv.style.height=chh+"px";ctx.setTransform(dpr,0,0,dpr,0,0)}
window.addEventListener("resize",()=>{sizeCv()});
const ML=36,MR=14,MT=14,MB=26;
function calcView(){const d=def(),[x0,x1]=d.xr(P),[lo,hi]=d.bounds(P);let mn=0,mx=0;for(let i=0;i<=120;i++){const y=d.f(lo+(hi-lo)*i/120,P);mn=Math.min(mn,y);mx=Math.max(mx,y)}
 d.handles(P).forEach(h=>{mn=Math.min(mn,h.y);mx=Math.max(mx,h.y)});const sp=(mx-mn)||1;return {x0,x1,y0:mn-.22*sp,y1:mx+.22*sp}}
const X=x=>ML+(x-V.x0)/(V.x1-V.x0)*(cw-ML-MR),Y=y=>MT+(V.y1-y)/(V.y1-V.y0)*(chh-MT-MB),iX=px=>V.x0+(px-ML)/(cw-ML-MR)*(V.x1-V.x0),iY=py=>V.y1-(py-MT)/(chh-MT-MB)*(V.y1-V.y0);
function piecePath(s){const d=def();ctx.beginPath();ctx.moveTo(X(s.a),Y(0));for(let i=0;i<=80;i++){const x=s.a+(s.b-s.a)*i/80;ctx.lineTo(X(x),Y(d.f(x,P)))}ctx.lineTo(X(s.b),Y(0));ctx.closePath()}
function curvePath(){const d=def();ctx.beginPath();for(let i=0;i<=240;i++){const x=V.x0+(V.x1-V.x0)*i/240,y=d.f(x,P);i?ctx.lineTo(X(x),Y(y)):ctx.moveTo(X(x),Y(y))}}
function niceStep(span){for(const s of [1,2,5,10,20,50,100,200,500,1000])if(span/s<=6)return s;return 1000}
function valStr(sign){const d=def();if(dragged||P.orig||!d.exactOK&&d.exactOK===false)return nf(sign>0?numPos(d,P):numNeg(d,P));try{const e=exact(d,P);return (sign>0?e.pos:e.neg).str()}catch(_){return nf(sign>0?numPos(d,P):numNeg(d,P))}}
function totStr(){const d=def();if(dragged||P.orig)return nf(numArea(d,P));try{return exact(d,P).tot.str()}catch(_){return nf(numArea(d,P))}}
function pill(k,text,x,y,sc,col){const on=window.HLK.includes(k),pul=.5+.5*Math.sin(performance.now()/150),fs=Math.round(15*sc);ctx.save();ctx.font=`800 ${fs}px "Malgun Gothic"`;const w=ctx.measureText(text).width+16,h=fs+10,px=clamp(x-w/2,2,cw-w-2),py=clamp(y-h/2,2,chh-h-2);
 ctx.fillStyle="rgba(8,14,30,.93)";ctx.strokeStyle=col;ctx.lineWidth=on?3.5:2;if(on){ctx.shadowColor=col;ctx.shadowBlur=16+14*pul}ctx.beginPath();ctx.roundRect(px,py,w,h,h/2);ctx.fill();ctx.stroke();ctx.shadowBlur=0;ctx.fillStyle=col;ctx.fillText(text,px+8,py+h/2+fs*.36);ctx.restore();window.PILLS.push({k,x:px,y:py,w,h})}
function draw(){const d=def();if(!d)return;V=frozen||calcView();const hk=window.HLK,sc=Math.max(.7,Math.min(1,cw/560));window.PILLS=[];
 ctx.clearRect(0,0,cw,chh);ctx.fillStyle="#0b1226";ctx.fillRect(0,0,cw,chh);
 ctx.save();ctx.beginPath();ctx.rect(ML-2,MT-2,cw-ML-MR+4,chh-MT-MB+4);ctx.clip();
 /* 격자 */
 ctx.strokeStyle="rgba(120,140,190,.14)";ctx.lineWidth=1;ctx.fillStyle="#7c8db0";ctx.font=`${Math.round(11*sc)}px sans-serif`;
 const xs=niceStep((V.x1-V.x0)/1),ys=niceStep(V.y1-V.y0);ctx.restore();
 for(let x=Math.ceil(V.x0/xs)*xs;x<=V.x1;x+=xs){ctx.beginPath();ctx.moveTo(X(x),MT);ctx.lineTo(X(x),chh-MB);ctx.stroke();if(!unk()&&x!==0)ctx.fillText(String(x),X(x)-4,Y(0)+14*sc)}
 for(let y=Math.ceil(V.y0/ys)*ys;y<=V.y1;y+=ys){ctx.beginPath();ctx.moveTo(ML,Y(y));ctx.lineTo(cw-MR,Y(y));ctx.stroke();if(!unk()&&y!==0)ctx.fillText(String(y),4,Y(y)+4)}
 ctx.save();ctx.beginPath();ctx.rect(ML-2,MT-2,cw-ML-MR+4,chh-MT-MB+4);ctx.clip();
 /* 축 */
 ctx.strokeStyle="#cbd5e1";ctx.lineWidth=1.8;ctx.beginPath();ctx.moveTo(ML,Y(0));ctx.lineTo(cw-MR,Y(0));ctx.stroke();
 if(V.x0<0&&V.x1>0){ctx.beginPath();ctx.moveTo(X(0),MT);ctx.lineTo(X(0),chh-MB);ctx.stroke()}
 const pcs=piecesNum(d,P);
 pcs.forEach(s=>{piecePath(s);ctx.fillStyle=(s.sign>0?COL.pos:COL.neg)+"44";ctx.fill()});
 curvePath();ctx.strokeStyle="#e8edf6";ctx.lineWidth=2.6;ctx.stroke();
 const [lo,hi]=d.bounds(P);ctx.setLineDash([6,5]);ctx.strokeStyle="#facc1599";ctx.lineWidth=1.8;[lo,hi].forEach(x=>{ctx.beginPath();ctx.moveTo(X(x),Y(0));ctx.lineTo(X(x),Y(d.f(x,P)));ctx.stroke()});ctx.setLineDash([]);
 /* 형광 */
 if(hk.length){ctx.fillStyle="rgba(5,8,18,.55)";ctx.fillRect(0,0,cw,chh);const pul=.5+.5*Math.sin(performance.now()/150);
  const glow=(col,fn)=>{ctx.save();ctx.shadowColor=col;ctx.shadowBlur=18+14*pul;fn();ctx.restore()};
  pcs.forEach(s=>{const k=s.sign>0?"pos":"neg";if(hk.includes(k)||hk.includes("S"))glow(COL[k],()=>{piecePath(s);ctx.fillStyle=COL[k]+"88";ctx.fill();ctx.strokeStyle=COL[k];ctx.lineWidth=2.5;ctx.stroke()})});
  if(hk.includes("f"))glow(COL.f,()=>{curvePath();ctx.strokeStyle=COL.f;ctx.lineWidth=4.5;ctx.stroke()});
  if(hk.includes("axis"))glow(COL.axis,()=>{ctx.strokeStyle=COL.axis;ctx.lineWidth=4.5;ctx.beginPath();ctx.moveTo(ML,Y(0));ctx.lineTo(cw-MR,Y(0));ctx.stroke()});
  [["lo",lo],["hi",hi]].forEach(([k,x])=>{if(hk.includes(k))glow(COL.axis,()=>{ctx.strokeStyle=COL.axis;ctx.lineWidth=4.5;ctx.beginPath();ctx.moveTo(X(x),MT);ctx.lineTo(X(x),chh-MB);ctx.stroke()})})}
 ctx.restore();
 /* 기호 이름 */
 (d.xl?d.xl(P):[]).forEach(o=>{ctx.fillStyle="#facc15";ctx.font=`800 ${Math.round(15*sc)}px "Malgun Gothic"`;ctx.fillText(o.t,X(o.x)-5,Y(0)+(d.f(o.x+.01,P)<d.f(o.x-.01,P)?-9:18*sc))});
 /* 손잡이 */
 const hs=d.handles(P),pul=.5+.5*Math.sin(performance.now()/200);
 hs.forEach(h=>{const x=X(h.x),y=Y(h.y);ctx.save();ctx.shadowColor="#facc15";ctx.shadowBlur=8+8*pul;ctx.fillStyle="#facc15";ctx.beginPath();ctx.arc(x,y,8,0,7);ctx.fill();ctx.restore();ctx.strokeStyle="#1b1500";ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y,8,0,7);ctx.stroke();
  if(h.n==="t"&&showSol){ctx.fillStyle="#facc15";ctx.font=`800 ${Math.round(13*sc)}px "Malgun Gothic"`;ctx.fillText("∫₁^"+h.x+" f = "+nf(d.F(h.x,P)-d.F(1,P)),x+10,Y(0)-10)}});
 /* 이름표 */
 const seen={};pcs.forEach(s=>{const k=s.sign>0?"pos":"neg",sym=s.sign>0?"S₁":"S₂",mx=(s.a+s.b)/2,my=d.f(mx,P)/2;const first=!seen[k];seen[k]=1;
  pill(k,sym+(showSol&&first?" = "+valStr(s.sign):""),X(mx),Y(my),sc,COL[k])});
 pill("S","S"+(showSol?" = "+totStr():""),cw-60,26,sc,COL.S)}
(function loop(){draw();requestAnimationFrame(loop)})();

/* ---------- 포인터 ---------- */
function pos(e){const r=cv.getBoundingClientRect();return [(e.clientX-r.left)*cw/r.width,(e.clientY-r.top)*chh/r.height]}
const hitH=(px,py)=>{if(!V)return null;const hs=def().handles(P);for(const h of hs)if(Math.hypot(X(h.x)-px,Y(h.y)-py)<=14)return h;return null};
const hitP=(px,py)=>window.PILLS.find(p=>px>=p.x&&px<=p.x+p.w&&py>=p.y&&py<=p.y+p.h);
cv.addEventListener("pointerdown",e=>{const [px,py]=pos(e),h=hitH(px,py);if(h){drag=h.n;frozen=V;try{cv.setPointerCapture(e.pointerId)}catch(_){}return}
 const p=hitP(px,py);if(p){const ks=[p.k];lockHL=(lockHL&&lockHL.join()===ks.join())?null:ks;recomputeHL()}});
cv.addEventListener("pointermove",e=>{const [px,py]=pos(e);if(drag){const h=def().handles(P).find(q=>q.n===drag);if(h){h.set(P,iX(px),iY(py));if(drag!=="t")dragged=true}return}
 const p=hitP(px,py),hh=hitH(px,py);cv.style.cursor=hh?"grab":p?"pointer":"default";const nh=(!hh&&p)?[p.k]:null;if((hoverHL&&hoverHL.join())!==(nh&&nh.join())){hoverHL=nh;recomputeHL()}});
const endDrag=()=>{drag=null;frozen=null};cv.addEventListener("pointerup",endDrag);cv.addEventListener("pointercancel",endDrag);
cv.addEventListener("pointerleave",()=>{if(!drag&&hoverHL){hoverHL=null;recomputeHL()}});

setMode(0);



/* ---------- 다른 풀이 ---------- */
const GEN={"0:0":"tot","0:1":"neg","0:2":"tot","0:3":"signed","1:0":"tot","1:1":"tot","1:3":"tot","2:0":"tot","2:1":"tot","2:2":"pos","2:3":"neg","4:1":"tot","5:1":"tot","5:2":"tot","5:3":"neg","6:0":"tot","6:1":"tot"};
function altTable(want){const d=def(),Pk=d.P(K),e=exact(d,Pk),pts=[e.segs[0].a,...e.segs.map(s=>s.b)],Fv=pts.map(x=>d.FrA(x,Pk)),v=x=>Fv[pts.findIndex(p=>p.str()===x.str())];
 const l1=`원시함수 F (단, F(0)=0)를 잡고 경계점마다 값을 구한다: `+pts.map((x,i)=>`F(${x.str()}) = ${Fv[i].str()}`).join(",  ");
 const l2=e.segs.map(s=>`[${s.a.str()}, ${s.b.str()}] ${s.sign>0?"x축 위":"x축 아래"}: ${s.sign>0?"":"−"}{F(${s.b.str()}) − F(${s.a.str()})} = ${s.area.str()}`).join(" ;  ");
 const r={tot:e.tot,neg:e.neg,pos:e.pos,signed:e.signed}[want],nm={tot:"넓이 S",neg:"x축 아래쪽 넓이",pos:"x축 위쪽 넓이",signed:"정적분의 값"}[want];
 return {t:"원시함수 값표로 한 번에",lines:[l1,l2,`${nm} = <b>${r.str()}</b>`]}}
function altList(){const key=cur+":"+mi,d=def(),o=[];
 if(GEN[key]){try{o.push(altTable(GEN[key]))}catch(_){}}
 const b=K.b,c=K.c,a=K.a,F=(n,dd)=>fr(n,dd).str();
 if(cur===1&&(mi===0||mi===1)){const ans=F(b**3,3);
  o.unshift({t:"(x−a)ⁿ 의 적분 공식 (전개 안 함)",lines:[`곡선은 y = −(x−${b})² 이므로 S = ∫_0^${b} (x−${b})² dx`,`∫(x−a)ⁿ dx = (x−a)ⁿ⁺¹/(n+1) 이므로 [(x−${b})³/3]_0^${b}`,`= 0 − (−${b})³/3 = <b>${ans}</b>`]},
  {t:"평행이동으로 간단한 식 만들기",lines:[`y = −(x−${b})² 은 y = −x² 을 x축 방향으로 ${b}만큼 옮긴 것이므로 넓이는 같다`,`y = −x² 과 x축, x = −${b}, x = 0 으로 둘러싸인 넓이로 바꿔도 같다: S = ∫_{−${b}}^0 x² dx`,`= [x³/3]_{−${b}}^0 = <b>${ans}</b>`]},
  {t:"포물선의 1/3 비 (적분 없이)",lines:[`접점 (${b}, 0), y절편 (0, −${b*b}) 로 가로 ${b}, 세로 ${b*b}인 직사각형을 만든다 (넓이 ${b**3})`,`포물선과 x축 사이 넓이는 이 직사각형의 1/3`,`S = ${b**3} × 1/3 = <b>${ans}</b>`]})}
 if(cur===1&&mi===3){const x=c-b;o.unshift({t:"(x−a)ⁿ 의 적분 공식",lines:[`S = ∫_0^${c} (x−${b})² dx = [(x−${b})³/3]_0^${c}`,`= {(${c}−${b})³ − (0−${b})³}/3 = (${x**3} + ${b**3})/3`,`= <b>${F(x**3+b**3,3)}</b>`]})}
 if(cur===3&&(mi===0||mi===1)){const P=PR[3].P(K),I1=mi?PR[3].I1(P):fr(7,3),I2=mi?PR[3].I2(P):fr(-1,2);o.unshift({t:"넓이의 뜻으로 읽기",lines:[`[0, α] 에서 f(0) = αβ > 0 이므로 f ≥ 0 → ∫_0^α f dx = ${I1.str()} 는 <b>x축 위쪽 넓이 A</b>`,`[α, β] 에서 f ≤ 0 이므로 ∫_0^β f dx = A − S  (S = 아래쪽 넓이)`,`${I2.str()} = ${I1.str()} − S → S = ${I1.str()} − (${I2.str()}) = <b>${I1.sub(I2).str()}</b>`]})}
 if(cur===4&&mi!==3){const s=mi===1?F(a**3,6):null;o.unshift({t:"이차함수 넓이 공식",lines:[`이차함수 y = ax² + bx + c 가 x축과 두 점 α, β 에서 만날 때 S = |a|(β−α)³/6`,`y = −x² + ${mi===1?a:"a"}x = −x(x−${mi===1?a:"a"}) 이므로 |a| = 1, α = 0, β = ${mi===1?a:"a"}`,mi===1?`S = (${a}−0)³/6 = <b>${s}</b>`:`a³/6 = ${F(K.a**3,6)} → a³ = ${K.a**3} → a = <b>${K.a}</b>`]},{t:"포물선의 2/3 비",lines:[`꼭짓점 (${mi===1?a:"a"}/2, ${mi===1?"a²/4":"a²/4"}), 밑변 ${mi===1?a:"a"} 인 직사각형(높이 = 꼭짓점의 y)을 만든다`,`포물선 아래 넓이는 이 직사각형의 2/3`,`S = 2/3 × ${mi===1?a:"a"} × ${mi===1?F(a*a,4):"a²/4"} = ${mi===1?"<b>"+s+"</b>":"a³/6 = "+F(K.a**3,6)+" → a = <b>"+K.a+"</b>"}`]})}
 if(cur===5&&mi<4){const p=K.p,q=K.q,k=K.k;o.unshift({t:"홀함수의 대칭 이용",lines:[`y = ${k===1?"":k}x³ 은 원점에 대하여 대칭 → x = 0 의 양쪽은 모양이 같고 부호만 반대`,...(mi===3?[`x축 아래쪽은 x < 0 쪽뿐이므로 ∫_{−${p}}^0 (−kx³) dx = k·${p}⁴/4`,`= ${k}·${p**4}/4 = <b>${F(k*p**4,4)}</b>`]:[`S = ∫_0^${p} |f| dx + ∫_0^${q} |f| dx = k·${p}⁴/4 + k·${q}⁴/4`,`= ${mi===0?"k × "+F(p**4+q**4,4)+" = "+PR[5].area(K).str()+" → k = <b>"+K.k+"</b>":"<b>"+F(k*(p**4+q**4),4)+"</b>"}`])]})}
 if(cur===6&&mi<2){const p=K.p,q=K.q,r=fr(q,p);o.unshift({t:"이차함수 넓이 공식",lines:[`양변을 미분하면 f(x) = ${polyStr([[p,2],[-q,1]])} = x(${polyStr([[p,1],[-q,0]])}) → 이차함수, x축과의 교점 0, ${r.str()}`,`S = |a|(β−α)³/6 = ${p}·(${r.str()})³/6`,`= <b>${exact(PR[6],PR[6].P(K)).tot.str()}</b>`]})}
 if(cur===2){const p=K.p,q=K.q,A1=fr(p**3*(p+2*q),12),A2=fr(q**3*(q+2*p),12),tot=A1.add(A2),w=mi===2?A1:mi===3?A2:tot,nm=mi===2?"x축 위쪽 넓이":mi===3?"x축 아래쪽 넓이":"S",al=-p,ga=q;
  const fin=mi===2?`${nm} = A₁ = <b>${w.str()}</b>`:mi===3?`${nm} = A₂ = <b>${w.str()}</b>`:`S = A₁ + A₂ = ${A1.str()} + ${A2.str()} = <b>${w.str()}</b>`;
  o.unshift({t:"삼차함수 넓이 공식 (두 근 사이 간격 p, q)",lines:[`삼차함수 y = (x−α)(x−β)(x−γ) (α<β<γ) 에서 p = β−α = ${p}, q = γ−β = ${q}`,`<b>A₁ = p³(p+2q)/12</b> = ${p**3}·${p+2*q}/12 = ${A1.str()} (x축 위),  <b>A₂ = q³(q+2p)/12</b> = ${q**3}·${q+2*p}/12 = ${A2.str()} (x축 아래)`,fin,`검산: ∫_{${al}}^{${ga}} f dx = (p−q)(p+q)³/12 = ${fr((p-q)*(p+q)**3,12).str()} = A₁ − A₂ = ${A1.sub(A2).str()}`]},
  {t:"(x−α)(x−β)² 와 (x−α)(x−β) 로 분해",lines:[`x − γ = (x − β) − q 이므로 f(x) = (x−α)(x−β)² − q(x−α)(x−β)`,`∫_α^β (x−α)(x−β)² dx = p⁴/12,  ∫_α^β (x−α)(x−β) dx = −p³/6  (1/12, 1/6 공식)`,`A₁ = p⁴/12 + q·p³/6 = ${p**4}/12 + ${q*p**3}/6 = <b>${A1.str()}</b>`,mi===2?`(위쪽 넓이 = A₁)`:`A₂ 는 x축 방향으로 뒤집어(x → −x) 같은 방법으로 q³(q+2p)/12 = <b>${A2.str()}</b>${mi===0||mi===1?",  S = <b>"+tot.str()+"</b>":""}`]})}
 if(cur===2&&K.p===K.q&&mi<2){const p=K.p,h=fr(p**4,2);o.push({t:"변곡점 대칭 (두 간격이 같을 때)",lines:[`p = q 이면 곡선은 가운데 근 β 에 대하여 점대칭 → A₁ = A₂`,`S = 2A₁ = 2·p³·3p/12 = p⁴/2 = <b>${h.str()}</b>`]})}
 /* ---- 추가 풀이들 ---- */
 try{
 if(GEN[key]==="tot"){const e=exact(d,d.P(K)),[lo,hi]=d.boundsFr(d.P(K));if(e.pos.n!==0&&e.neg.n!==0){o.push({t:"상쇄 보정: S = ∫f dx + 2 × (x축 아래쪽 넓이)",lines:[`∫ f dx 는 위쪽(+)에서 아래쪽(−)이 빠진 값: ∫_{${lo.str()}}^{${hi.str()}} f dx = 위쪽 − 아래쪽 = ${e.signed.str()}`,`넓이 S = 위쪽 + 아래쪽 = (위쪽 − 아래쪽) + 2 × 아래쪽`,`아래쪽 넓이 = ${e.neg.str()} 이므로 S = ${e.signed.str()} + 2 × ${e.neg.str()} = <b>${e.tot.str()}</b>`]})}}
 if(cur===0&&mi<2&&2*K.hi===K.c&&K.lo<=0){const c=K.c,e=exact(PR[0],PR[0].P(K)),h=fr(c**3,12);o.push({t:"포물선의 대칭 이용 (꼭짓점이 구간의 끝)",lines:[`y = x² − ${c}x 의 꼭짓점은 x = ${c}/2 = ${K.hi} 이고, 0 ≤ x ≤ ${c} 에서 x축 아래 부분 전체의 넓이는 이차함수 공식으로 ${c}³/6 = ${fr(c**3,6).str()}`,`대칭이므로 [0, ${K.hi}] 의 아래쪽 넓이는 그 절반 = ${c}³/12 = <b>${h.str()}</b>`,mi===1?`x축 아래쪽 부분의 넓이 = <b>${h.str()}</b>`:`[${K.lo}, 0] 의 위쪽 넓이 = ∫_{${K.lo}}^0 (x² − ${c}x) dx = ${e.pos.str()} → S = ${e.pos.str()} + ${h.str()} = <b>${e.tot.str()}</b>`]})}
 if(cur===1&&mi===2){o.push({t:"포물선의 1/3 비로 b 구하기",lines:[`접점 (b, 0), y절편 (0, −b²) 인 직사각형(가로 b, 세로 b²)의 1/3 이 넓이`,`b³/3 = ${F(K.b**3,3)}`,`b³ = ${K.b**3} → b = <b>${K.b}</b>`]})}
 if(cur===3&&mi<2){const P=PR[3].P(K),I1=mi?PR[3].I1(P):fr(7,3),I2=mi?PR[3].I2(P):fr(-1,2);
  o.push({t:"적분함수 F(x) = ∫₀ˣ f(t)dt 의 극댓값 − 극솟값",lines:[`F'(x) = f(x) = (x−α)(x−β) 이므로 F 는 x = α 에서 극대, x = β 에서 극소`,`F(α) = ∫_0^α f dx = ${I1.str()},  F(β) = ∫_0^β f dx = ${I2.str()}`,`S = −∫_α^β f dx = F(α) − F(β) = ${I1.str()} − (${I2.str()}) = <b>${I1.sub(I2).str()}</b>`]});
  o.push(mi===0?{t:"이차함수 넓이 공식으로 검산",lines:[`S = (β−α)³/6 = 17/6 이면 (β−α)³ = 17, β − α = ∛17 ≈ ${nf(Math.cbrt(17))}`,`두 조건식을 풀어 얻은 α ≈ ${nf(AB0[0])}, β ≈ ${nf(AB0[1])} → β − α ≈ ${nf(AB0[1]-AB0[0])}  (일치)`,`그러므로 S = <b>17/6</b>`]}:{t:"이차함수 넓이 공식으로 검산",lines:[`숨은 α = ${K.al}, β = ${K.be} 이면 S = (β−α)³/6 = ${K.be-K.al}³/6 = ${F((K.be-K.al)**3,6)}`,`조건에서 구한 ∫₀^α f − ∫₀^β f = ${I1.sub(I2).str()} 와 같다`,`그러므로 S = <b>${I1.sub(I2).str()}</b>`]})}
 if(cur===4&&mi<3){const A=mi===1?K.a:"a",s=mi===1?F(K.a**3,6):null;o.push({t:"대칭축으로 평행이동 (t = x − a/2)",lines:[`y = −(x − a/2)² + a²/4 이므로 t = x − a/2 로 놓으면 y = a²/4 − t², −a/2 ≤ t ≤ a/2`,`S = 2∫_0^{a/2} (a²/4 − t²) dt = 2[a²t/4 − t³/3]_0^{a/2} = 2(a³/8 − a³/24)`,`= a³/6${mi===1?` = ${K.a}³/6 = <b>${s}</b>`:` = ${F(K.a**3,6)} → a³ = ${K.a**3} → a = <b>${K.a}</b>`}`]})}
 if(cur===4&&mi===3){o.push({t:"미분으로 꼭짓점 구하기",lines:[`f(x) = −x² + ax → f'(x) = −2x + a = 0 → x = a/2 (꼭짓점의 x좌표)`,`f(a/2) = a²/4  (a = ${K.a} : 넓이 a³/6 = ${F(K.a**3,6)} 에서)`,`= ${K.a}²/4 = <b>${F(K.a*K.a,4)}</b>`]})}
 if(cur===5&&mi===0){const p=K.p,q=K.q;o.push({t:"원시함수 F(x) = kx⁴/4 로 한 번에",lines:[`F(−${p}) = k·${p}⁴/4,  F(0) = 0,  F(${q}) = k·${q}⁴/4`,`S = −{F(0) − F(−${p})} + {F(${q}) − F(0)} = F(−${p}) + F(${q}) = k(${p**4} + ${q**4})/4`,`${F(p**4+q**4,4)}·k = ${PR[5].area(K).str()} → k = <b>${K.k}</b>`]})}
 if(cur===6&&mi<2){const p=K.p,q=K.q,P={p,q},r=fr(q,p),G=x=>PR[6].FrA(x,P).sub(PR[6].FrA(fr(1),P));o.push({t:"주어진 적분 식에 직접 대입",lines:[`G(x) = ∫_1^x f(t)dt = ${PR[6].G(K)} 이고 f(x)=G'(x) 에서 x축과의 교점은 x = 0, ${r.str()}`,`[0, ${r.str()}] 에서 f ≤ 0 이므로 S = −∫_0^{${r.str()}} f dx = −{G(${r.str()}) − G(0)} = G(0) − G(${r.str()})`,`G(0) = ${G(Z).str()},  G(${r.str()}) = ${G(r).str()} → S = <b>${G(Z).sub(G(r)).str()}</b>`]})}
 }catch(e){}
 return o}
$("#bAlt").onclick=()=>{const box=$("#alt"),on=box.style.display==="block";if(on){box.style.display="none";$("#bAlt").textContent="다른 풀이";return}
 const L=altList();box.innerHTML=L.length?L.map((m,i)=>`<div class="altm"><div class="altt">다른 풀이 ${i+1} · ${m.t}</div>${m.lines.map((l,j)=>`<div style="margin:4px 0">${"①②③④"[j]} ${fmt(l)}</div>`).join("")}</div>`).join(""):`<div class="altm">이 문제는 기본 풀이가 가장 간단해요. (다른 문제나 변형에서 다른 풀이를 볼 수 있어요)</div>`;
 box.style.display="block";$("#bAlt").textContent="다른 풀이 접기"}







