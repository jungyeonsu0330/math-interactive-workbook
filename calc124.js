/* 미적분Ⅰ 124쪽 · 유형 01 곡선과 x축 사이의 넓이 (0815~0821) */
const $=s=>document.querySelector(s),PI=Math.PI,clamp=(v,l,h)=>Math.max(l,Math.min(h,v));
const gcd=(a,b)=>b?gcd(b,a%b):Math.abs(a);
class Fr{constructor(n,d=1){if(d<0){n=-n;d=-d}const g=gcd(n,d)||1;this.n=n/g;this.d=d/g}
 add(o){return new Fr(this.n*o.d+o.n*this.d,this.d*o.d)}sub(o){return new Fr(this.n*o.d-o.n*this.d,this.d*o.d)}mul(o){return new Fr(this.n*o.n,this.d*o.d)}div(o){return new Fr(this.n*o.d,this.d*o.n)}
 neg(){return new Fr(-this.n,this.d)}abs(){return new Fr(Math.abs(this.n),this.d)}val(){return this.n/this.d}str(){const s=this.d===1?String(Math.abs(this.n)):Math.abs(this.n)+"/"+this.d;return (this.n<0?"−":"")+s}}
const fr=(n,d)=>new Fr(n,d===undefined?1:d),Z=fr(0),pw=(x,k)=>{let r=fr(1);for(let i=0;i<k;i++)r=r.mul(x);return r};
const nf=x=>String(Math.round(x*100)/100),sg=n=>n<0?"−"+(-n):String(n);
const hk=(key,txt,cls)=>`<span class="hk${cls?" "+cls:""}" data-hl="${key}">${txt}</span>`,kk=t=>`<b class="k">${t}</b>`;
function polyStr(terms){let s="";terms.forEach(([c,e])=>{const v=c instanceof Fr?c:fr(c);if(v.n===0)return;const a=v.abs();let body=a.str();if(e>0){if(a.d===1&&a.n===1)body="";else if(a.d!==1)body="("+a.str()+")"}
 const xs=e===0?"":e===1?"x":"x"+"²³⁴"[e-2];const term=body+xs;if(!s)s=(v.n<0?"−":"")+term;else s+=(v.n<0?" − ":" + ")+term});return s||"0"}
const simpson=(g,a,b,n=20000)=>{if(a===b)return 0;const h=(b-a)/n;let s=g(a)+g(b);for(let i=1;i<n;i++)s+=g(a+i*h)*(i%2?4:2);return s*h/3};

/* ---------- 정확한 넓이 (분수) / 수치 넓이 ---------- */
function exact(def,P){const [lo,hi]=def.boundsFr(P);const rs=def.rootsFr(P).filter(r=>r.val()>lo.val()+1e-12&&r.val()<hi.val()-1e-12).sort((a,b)=>a.val()-b.val());const bp=[lo,...rs,hi],segs=[];
 for(let i=0;i<bp.length-1;i++){const a=bp[i],b=bp[i+1],mid=(a.val()+b.val())/2,sign=def.f(mid,P)>=0?1:-1,d=def.FrA(b,P).sub(def.FrA(a,P));segs.push({a,b,sign,area:d.mul(fr(sign))})}
 const m=[];for(const s of segs){const l=m[m.length-1];if(l&&l.sign===s.sign){l.b=s.b;l.area=l.area.add(s.area)}else m.push({...s})}
 let pos=Z,neg=Z;m.forEach(s=>{if(s.sign>0)pos=pos.add(s.area);else neg=neg.add(s.area)});return {segs:m,pos,neg,tot:pos.add(neg),signed:pos.sub(neg)}}
function piecesNum(def,P){const [lo,hi]=def.bounds(P);const rs=def.roots(P).filter(r=>r>lo+1e-9&&r<hi-1e-9).sort((a,b)=>a-b),bp=[lo,...rs,hi],segs=[];
 for(let i=0;i<bp.length-1;i++){const a=bp[i],b=bp[i+1],sign=def.f((a+b)/2,P)>=0?1:-1;segs.push({a,b,sign,area:sign*(def.F(b,P)-def.F(a,P))})}
 const m=[];for(const s of segs){const l=m[m.length-1];if(l&&l.sign===s.sign){l.b=s.b;l.area+=s.area}else m.push({...s})}return m}
const numArea=(def,P)=>{const [lo,hi]=def.bounds(P);return simpson(x=>Math.abs(def.f(x,P)),lo,hi)};
const numNeg=(def,P)=>{const [lo,hi]=def.bounds(P);return simpson(x=>Math.max(-def.f(x,P),0),lo,hi)};
const numPos=(def,P)=>{const [lo,hi]=def.bounds(P);return simpson(x=>Math.max(def.f(x,P),0),lo,hi)};
const numSigned=(def,P)=>{const [lo,hi]=def.bounds(P);return simpson(x=>def.f(x,P),lo,hi)};
/* 수치 이분법: 수치 넓이가 A 가 되는 매개변수 (독립 검증용) */
function bisect(g,lo,hi,target){for(let i=0;i<80;i++){const m=(lo+hi)/2;(g(m)<target)?lo=m:hi=m}return (lo+hi)/2}

/* ---------- 풀이 문장(일반) ---------- */
function solGen(def,P,want){const e=exact(def,P),[lo,hi]=def.boundsFr(P),rs=def.rootsFr(P),inside=rs.filter(r=>r.val()>lo.val()+1e-12&&r.val()<hi.val()-1e-12);
 const l1=`${def.fx(P)} → f(x) = 0 의 근: x = ${rs.map(r=>r.str()).join(", ")}.  구간 [${lo.str()}, ${hi.str()}] 안에서 부호가 바뀌는 곳: ${inside.length?"x = "+inside.map(r=>r.str()).join(", "):"없음"}`;
 const l2=e.segs.map(s=>`[${s.a.str()}, ${s.b.str()}] ${s.sign>0?"x축 위 → ∫ f dx":"x축 아래 → −∫ f dx"} = ${s.area.str()}`).join(" ;  ");
 let l3;if(want==="tot")l3=`S = ${e.segs.map(s=>s.area.str()).join(" + ")} = <b>${e.tot.str()}</b>`;else if(want==="neg")l3=`x축 아래쪽 넓이 = <b>${e.neg.str()}</b>`;else if(want==="pos")l3=`x축 위쪽 넓이 = <b>${e.pos.str()}</b>`;
 else l3=`∫ f dx = (x축 위 넓이) − (x축 아래 넓이) = ${e.pos.str()} − ${e.neg.str()} = <b>${e.signed.str()}</b>  (넓이 ${e.tot.str()} 와 다르다!)`;
 return [l1,l2,l3]}

/* ---------- 문제 정의 ---------- */
const PR=[];
const wrapK=(K0,mods)=>mods;
/* 0815 */
PR.push({id:"0815",tag:"대표문제",K0:{lo:-1,hi:3,c:6},L:{lo:"구간 시작",hi:"구간 끝",c:"c (y=x²−cx)"},
 P:K=>({lo:K.lo,hi:K.hi,c:K.c}),f:(x,P)=>x*x-P.c*x,F:(x,P)=>x*x*x/3-P.c*x*x/2,FrA:(x,P)=>pw(x,3).div(fr(3)).sub(fr(P.c).mul(pw(x,2)).div(fr(2))),
 roots:P=>[0,P.c],rootsFr:P=>[Z,fr(P.c)],bounds:P=>[P.lo,P.hi],boundsFr:P=>[fr(P.lo),fr(P.hi)],xr:P=>[Math.min(P.lo,0)-1.5,Math.max(P.hi,P.c)+1.5],
 fx:P=>"y = "+polyStr([[1,2],[-P.c,1]]),
 handles:P=>[{n:"lo",x:P.lo,y:0,set:(P,x)=>{P.lo=clamp(Math.round(x),-6,P.hi-1)}},{n:"hi",x:P.hi,y:0,set:(P,x)=>{P.hi=clamp(Math.round(x),P.lo+1,9)}}],
 ok:K=>Number.isInteger(K.lo)&&Number.isInteger(K.hi)&&Number.isInteger(K.c)&&K.lo<K.hi&&K.lo>=-6&&K.hi<=9&&K.c>=1&&K.c<=8,
 txt:(K,what)=>`구간 [${sg(K.lo)}, ${sg(K.hi)}]에서 곡선 ${hk("f","y = "+polyStr([[1,2],[-K.c,1]]))}와 ${hk("axis","x축")} 및 두 직선 ${hk("lo","x = "+sg(K.lo))}, ${hk("hi","x = "+sg(K.hi))}으로 둘러싸인 도형 ${what}`,
 modes:[
  {n:"원래 문제",K:{lo:-1,hi:3,c:6},hl:["S"],ask:"tot",text:K=>PR[0].txt(K,`의 ${hk("S","넓이","g")}를 구하시오.`),ans:K=>({fr:exact(PR[0],PR[0].P(K)).tot}),sol:K=>solGen(PR[0],PR[0].P(K),"tot")},
  {n:"x축 아래쪽 넓이",d:"전체가 아니라 x축 아래쪽 부분만 구해요.",K:{lo:-1,hi:3,c:6},hl:["neg"],text:K=>PR[0].txt(K,`중 ${hk("neg","x축 아래쪽 부분","g")}의 넓이를 구하시오.`),ans:K=>({fr:exact(PR[0],PR[0].P(K)).neg}),sol:K=>solGen(PR[0],PR[0].P(K),"neg"),num:K=>numNeg(PR[0],PR[0].P(K))},
  {n:"구간·곡선 바꾸기",d:"구간과 계수를 바꿔서 같은 방식으로 넓이를 구해요.",K:{lo:-2,hi:5,c:4},hl:["S"],text:K=>PR[0].txt(K,`의 ${hk("S","넓이","g")}를 구하시오.`),ans:K=>({fr:exact(PR[0],PR[0].P(K)).tot}),sol:K=>solGen(PR[0],PR[0].P(K),"tot"),num:K=>numArea(PR[0],PR[0].P(K))},
  {n:"∫f dx 와 넓이의 차이",d:"정적분의 값과 넓이가 왜 다른지 비교해요.",K:{lo:-1,hi:3,c:6},hl:["pos","neg"],text:K=>`곡선 ${hk("f","y = "+polyStr([[1,2],[-K.c,1]]))}에 대하여 정적분 ${hk("S","∫_{"+sg(K.lo)+"}^{"+sg(K.hi)+"} (x² − "+K.c+"x) dx","g")}의 값은?`,ans:K=>({fr:exact(PR[0],PR[0].P(K)).signed}),sol:K=>solGen(PR[0],PR[0].P(K),"signed"),num:K=>numSigned(PR[0],PR[0].P(K))}]});
/* 0816 */
PR.push({id:"0816",tag:"",K0:{b:3},L:{b:"접점의 x좌표 b",c:"직선 x = c"},bookChoices:["6","7","8","9","10"],bookIdx:3,
 P:K=>({b:K.b,hi:K.c!==undefined?K.c:K.b,tie:K.c===undefined}),f:(x,P)=>-(x-P.b)*(x-P.b),F:(x,P)=>-Math.pow(x-P.b,3)/3,FrA:(x,P)=>pw(x.sub(fr(P.b)),3).div(fr(3)).neg(),
 roots:P=>[P.b],rootsFr:P=>[fr(P.b)],bounds:P=>[0,P.hi],boundsFr:P=>[Z,fr(P.hi)],xr:P=>[-1.5,Math.max(P.hi,P.b)+1.6],
 fx:P=>"y = "+polyStr([[-1,2],[2*P.b,1],[-P.b*P.b,0]]),
 handles:P=>{const h=[{n:"b",x:P.b,y:0,set:(P,x)=>{P.b=clamp(Math.round(x),1,7);if(P.tie)P.hi=P.b}}];if(!P.tie)h.push({n:"hi",x:P.hi,y:0,set:(P,x)=>{P.hi=clamp(Math.round(x),P.b+1,10)}});return h},
 ok:K=>Number.isInteger(K.b)&&K.b>=1&&K.b<=7&&(K.c===undefined||(Number.isInteger(K.c)&&K.c>K.b&&K.c<=10)),
 modes:[
  {n:"원래 문제",K:{b:3},hl:["S"],text:K=>`곡선 ${hk("f","y = −x² + "+(2*K.b)+"x − "+(K.b*K.b))}와 ${hk("axis","x축")} 및 ${hk("lo","y축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}는?`,ans:K=>({fr:exact(PR[1],PR[1].P(K)).tot}),sol:K=>[`곡선은 −(x−${K.b})² 이므로 x축과 x = ${K.b} 에서 접해요 (교점 x = ${K.b})`,`x = 0 (y축)에서 x = ${K.b} 까지 곡선이 x축 아래 → S = −∫₀^${K.b} (−x² + ${2*K.b}x − ${K.b*K.b}) dx`,`= <b>${exact(PR[1],PR[1].P(K)).tot.str()}</b>`]},
  {n:"다른 포물선",d:"접점이 바뀐 포물선의 넓이를 구해요.",K:{b:4},hl:["S"],text:K=>`곡선 ${hk("f","y = −x² + "+(2*K.b)+"x − "+(K.b*K.b))}와 ${hk("axis","x축")} 및 ${hk("lo","y축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,ans:K=>({fr:exact(PR[1],PR[1].P(K)).tot}),sol:K=>[`−(x−${K.b})² → x = ${K.b} 에서 접해요`,`S = −∫₀^${K.b} (−(x−${K.b})²) dx = ∫₀^${K.b} (x−${K.b})² dx = [(x−${K.b})³/3]`,`= <b>${exact(PR[1],PR[1].P(K)).tot.str()}</b>`],num:K=>numArea(PR[1],PR[1].P(K))},
  {n:"넓이로 b 구하기",d:"조건을 뒤집어요: 넓이를 주고 접점 b 를 구해요.",K:{b:3},hl:["S"],ok:K=>K.b>=1,text:K=>`곡선 ${hk("f","y = −x² + 2bx − b²")} (b > 0)과 ${hk("axis","x축")} 및 ${hk("lo","y축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}가 ${kk(fr(K.b**3,3).str())}일 때, b의 값을 구하시오.`,ans:K=>({fr:fr(K.b)}),sol:K=>[`곡선 −(x−b)² 는 x = b 에서 x축에 접해요`,`S = ∫₀^b (x−b)² dx = b³/3 = ${fr(K.b**3,3).str()}`,`b³ = ${K.b**3} → b = <b>${K.b}</b>`],numRev:K=>bisect(b=>numArea(PR[1],{b,hi:b,tie:true}),0.01,20,K.b**3/3)},
  {n:"직선 x = c 까지",d:"x축·y축에 직선 x = c 가 더해져 구간이 달라져요.",K:{b:3,c:5},hl:["S","hi"],text:K=>`곡선 ${hk("f","y = −x² + "+(2*K.b)+"x − "+(K.b*K.b))}와 ${hk("axis","x축")}, ${hk("lo","y축")} 및 직선 ${hk("hi","x = "+K.c)}로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,ans:K=>({fr:exact(PR[1],PR[1].P(K)).tot}),sol:K=>[`곡선은 x = ${K.b} 에서 x축에 접하고 [0, ${K.c}] 에서 모두 x축 아래 (부호가 바뀌지 않아요)`,`S = ∫₀^${K.c} (x−${K.b})² dx = [(x−${K.b})³/3]₀^${K.c} = ((${K.c}−${K.b})³ + ${K.b}³)/3`,`= <b>${exact(PR[1],PR[1].P(K)).tot.str()}</b>`],num:K=>numArea(PR[1],PR[1].P(K))}]});
/* 0817 */
PR.push({id:"0817",tag:"",K0:{p:2,q:1},L:{p:"왼쪽 근 −p",q:"오른쪽 근 q"},bookChoices:["3/2","2","37/12","10/3","4"],bookIdx:2,
 P:K=>({p:K.p,q:K.q}),f:(x,P)=>(x+P.p)*x*(x-P.q),F:(x,P)=>x*x*x*x/4+(P.p-P.q)*x*x*x/3-P.p*P.q*x*x/2,
 FrA:(x,P)=>pw(x,4).div(fr(4)).add(fr(P.p-P.q).mul(pw(x,3)).div(fr(3))).sub(fr(P.p*P.q).mul(pw(x,2)).div(fr(2))),
 roots:P=>[-P.p,0,P.q],rootsFr:P=>[fr(-P.p),Z,fr(P.q)],bounds:P=>[-P.p,P.q],boundsFr:P=>[fr(-P.p),fr(P.q)],xr:P=>[-P.p-1.4,P.q+1.4],
 fx:P=>"y = "+polyStr([[1,3],[P.p-P.q,2],[-P.p*P.q,1]]),
 handles:P=>[{n:"pl",x:-P.p,y:0,set:(P,x)=>{P.p=clamp(Math.round(-x),1,5)}},{n:"qr",x:P.q,y:0,set:(P,x)=>{P.q=clamp(Math.round(x),1,5)}}],
 ok:K=>Number.isInteger(K.p)&&Number.isInteger(K.q)&&K.p>=1&&K.p<=5&&K.q>=1&&K.q<=5,
 txt:(K,what)=>`곡선 ${hk("f","y = "+polyStr([[1,3],[K.p-K.q,2],[-K.p*K.q,1]]))}와 ${hk("axis","x축")}으로 둘러싸인 도형 ${what}`,
 modes:[
  {n:"원래 문제",K:{p:2,q:1},hl:["S"],text:K=>PR[2].txt(K,`의 ${hk("S","넓이","g")}는?`),ans:K=>({fr:exact(PR[2],PR[2].P(K)).tot}),sol:K=>solGen(PR[2],PR[2].P(K),"tot")},
  {n:"다른 삼차곡선",d:"근의 위치가 다른 삼차곡선의 넓이를 구해요.",K:{p:3,q:1},hl:["S"],text:K=>PR[2].txt(K,`의 ${hk("S","넓이","g")}를 구하시오.`),ans:K=>({fr:exact(PR[2],PR[2].P(K)).tot}),sol:K=>solGen(PR[2],PR[2].P(K),"tot"),num:K=>numArea(PR[2],PR[2].P(K))},
  {n:"x축 위쪽 넓이",d:"x축 위쪽 부분만 구해요.",K:{p:2,q:1},hl:["pos"],text:K=>PR[2].txt(K,`중 ${hk("pos","x축 위쪽 부분","g")}의 넓이를 구하시오.`),ans:K=>({fr:exact(PR[2],PR[2].P(K)).pos}),sol:K=>solGen(PR[2],PR[2].P(K),"pos"),num:K=>numPos(PR[2],PR[2].P(K))},
  {n:"x축 아래쪽 넓이",d:"x축 아래쪽 부분만 구해요.",K:{p:2,q:1},hl:["neg"],text:K=>PR[2].txt(K,`중 ${hk("neg","x축 아래쪽 부분","g")}의 넓이를 구하시오.`),ans:K=>({fr:exact(PR[2],PR[2].P(K)).neg}),sol:K=>solGen(PR[2],PR[2].P(K),"neg"),num:K=>numNeg(PR[2],PR[2].P(K))}]});
/* 0818 : α, β 는 주어진 적분값에서 수치로 구한다 */
const solveAB=()=>{let a=1.2,b=3;for(let it=0;it<200;it++){const g1=a*a*(3*b-a)/6-7/3,g2=b*b*(3*a-b)/6+1/2;const e=1e-6,d11=(((a+e)**2*(3*b-a-e)/6-7/3)-g1)/e,d12=((a*a*(3*(b+e)-a)/6-7/3)-g1)/e,d21=((((b)**2*(3*(a+e)-b)/6+.5))-(g2))/e,d22=(((b+e)**2*(3*a-b-e)/6+.5)-g2)/e,det=d11*d22-d12*d21;if(Math.abs(det)<1e-12)break;a-=(g1*d22-g2*d12)/det;b-=(d11*g2-d21*g1)/det}return [a,b]};
const AB0=solveAB();
PR.push({id:"0818",tag:"",K0:{orig:1},L:{al:"α",be:"β"},
 P:K=>K.orig?{al:AB0[0],be:AB0[1],orig:true}:{al:K.al,be:K.be},f:(x,P)=>(x-P.al)*(x-P.be),F:(x,P)=>x*x*x/3-(P.al+P.be)*x*x/2+P.al*P.be*x,
 FrA:(x,P)=>pw(x,3).div(fr(3)).sub(fr(P.al+P.be).mul(pw(x,2)).div(fr(2))).add(fr(P.al*P.be).mul(x)),
 roots:P=>[P.al,P.be],rootsFr:P=>[fr(P.al),fr(P.be)],bounds:P=>[P.al,P.be],boundsFr:P=>[fr(P.al),fr(P.be)],exactOK:P=>!P.orig&&Number.isInteger(P.al)&&Number.isInteger(P.be),xr:P=>[-0.8,P.be+1.4],
 fx:P=>P.orig?"y = (x − α)(x − β)":"y = "+polyStr([[1,2],[-(P.al+P.be),1],[P.al*P.be,0]]),
 handles:P=>[{n:"al",x:P.al,y:0,set:(P,x)=>{P.al=clamp(Math.round(x*10)/10,0.2,P.be-0.4);P.orig=false}},{n:"be",x:P.be,y:0,set:(P,x)=>{P.be=clamp(Math.round(x*10)/10,P.al+0.4,9);P.orig=false}}],
 ok:K=>K.orig||(Number.isInteger(K.al)&&Number.isInteger(K.be)&&K.al>=1&&K.be>K.al&&K.be<=8),
 I1:P=>fr(P.al*P.al*(3*P.be-P.al),6),I2:P=>fr(P.be*P.be*(3*P.al-P.be),6),
 modes:[
  {n:"원래 문제",K:{orig:1},hl:["S"],text:K=>`두 양수 α, β (α < β)에 대하여 함수 ${hk("f","f(x) = (x − α)(x − β)")}라 하면 ∫₀^α f(x)dx = ${kk("7/3")}, ∫₀^β f(x)dx = ${kk("−1/2")}일 때, 곡선 y = f(x)와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,
   ans:K=>({fr:fr(17,6)}),sol:K=>[`f(x)=0 의 근 x = α, β → 둘러싸인 도형은 [α, β] 에서 x축 아래`,`S = −∫_α^β f dx = −{∫₀^β f dx − ∫₀^α f dx} = ∫₀^α f dx − ∫₀^β f dx`,`= 7/3 − (−1/2) = <b>17/6</b>`],num:K=>numArea(PR[3],PR[3].P(K))},
  {n:"다른 적분값",d:"적분값이 다른 경우(α, β 는 숨겨져 있어요)의 넓이를 구해요.",K:{al:1,be:4},hl:["S"],text:K=>{const P=PR[3].P(K);return `두 양수 α, β (α < β)에 대하여 함수 ${hk("f","f(x) = (x − α)(x − β)")}라 하면 ∫₀^α f(x)dx = ${kk(PR[3].I1(P).str())}, ∫₀^β f(x)dx = ${kk(PR[3].I2(P).str())}일 때, 곡선 y = f(x)와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`},
   ans:K=>{const P=PR[3].P(K);return {fr:PR[3].I1(P).sub(PR[3].I2(P))}},sol:K=>{const P=PR[3].P(K);return [`둘러싸인 도형은 [α, β] 에서 x축 아래`,`S = −∫_α^β f dx = ∫₀^α f dx − ∫₀^β f dx`,`= ${PR[3].I1(P).str()} − (${PR[3].I2(P).str()}) = <b>${PR[3].I1(P).sub(PR[3].I2(P)).str()}</b>`]},num:K=>numArea(PR[3],PR[3].P(K))},
  {n:"∫_α^β f dx 의 값",d:"넓이가 아니라 부호 있는 정적분의 값을 구해요.",K:{al:2,be:5},hl:["S"],text:K=>{const P=PR[3].P(K);return `두 양수 α, β (α < β)에 대하여 함수 ${hk("f","f(x) = (x − α)(x − β)")}라 하면 ∫₀^α f(x)dx = ${kk(PR[3].I1(P).str())}, ∫₀^β f(x)dx = ${kk(PR[3].I2(P).str())}일 때, ${hk("S","∫_α^β f(x)dx","g")}의 값은?`},
   ans:K=>{const P=PR[3].P(K);return {fr:PR[3].I2(P).sub(PR[3].I1(P))}},sol:K=>{const P=PR[3].P(K);return [`∫_α^β f dx = ∫₀^β f dx − ∫₀^α f dx`,`= ${PR[3].I2(P).str()} − ${PR[3].I1(P).str()}`,`= <b>${PR[3].I2(P).sub(PR[3].I1(P)).str()}</b>  (x축 아래라서 음수, 넓이는 ${PR[3].I1(P).sub(PR[3].I2(P)).str()})`]},num:K=>numSigned(PR[3],PR[3].P(K))},
  {n:"넓이로 β − α 구하기",d:"조건을 뒤집어요: 넓이를 주고 근 사이의 거리를 구해요.",K:{al:1,be:4},hl:["S"],text:K=>`두 양수 α, β (α < β)에 대하여 함수 ${hk("f","f(x) = (x − α)(x − β)")}와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}가 ${kk(fr((K.be-K.al)**3,6).str())}일 때, β − α의 값을 구하시오.`,
   ans:K=>({fr:fr(K.be-K.al)}),sol:K=>[`S = |∫_α^β (x−α)(x−β) dx| = (β−α)³/6  (이차함수와 x축 사이 넓이 공식)`,`(β−α)³/6 = ${fr((K.be-K.al)**3,6).str()} → (β−α)³ = ${(K.be-K.al)**3}`,`β − α = <b>${K.be-K.al}</b>`],numRev:K=>bisect(d=>numArea(PR[3],{al:1,be:1+d}),0.01,20,(K.be-K.al)**3/6)}]});
/* 0819 */
PR.push({id:"0819",tag:"",K0:{a:4},L:{a:"a (y=−x²+ax)"},bookChoices:["7/2","4","9/2","5","11/2"],bookIdx:1,
 P:K=>({a:K.a}),f:(x,P)=>-x*x+P.a*x,F:(x,P)=>-x*x*x/3+P.a*x*x/2,FrA:(x,P)=>pw(x,3).div(fr(3)).neg().add(fr(P.a).mul(pw(x,2)).div(fr(2))),
 roots:P=>[0,P.a],rootsFr:P=>[Z,fr(P.a)],bounds:P=>[0,P.a],boundsFr:P=>[Z,fr(P.a)],xr:P=>[-1.4,P.a+1.6],fx:P=>"y = "+polyStr([[-1,2],[P.a,1]]),
 handles:P=>[{n:"a",x:P.a,y:0,set:(P,x)=>{P.a=clamp(Math.round(x),1,9)}}],ok:K=>Number.isInteger(K.a)&&K.a>=1&&K.a<=9,
 modes:[
  {n:"원래 문제",K:{a:4},hl:["S"],text:K=>`곡선 ${hk("f","y = −x² + ax")}와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}가 ${kk(fr(K.a**3,6).str())}일 때, 양수 a의 값은?`,ans:K=>({fr:fr(K.a)}),sol:K=>[`−x² + ax = 0 → x = 0 또는 x = a`,`S = ∫₀^a (−x² + ax) dx = [−x³/3 + a x²/2]₀^a = a³/6`,`a³/6 = ${fr(K.a**3,6).str()} → a³ = ${K.a**3} → a = <b>${K.a}</b>`],numRev:K=>bisect(a=>numArea(PR[4],{a}),0.1,20,K.a**3/6)},
  {n:"a가 주어질 때 넓이",d:"조건을 뒤집어요: a 를 주고 넓이를 구해요.",K:{a:5},hl:["S"],text:K=>`곡선 ${hk("f","y = −x² + "+K.a+"x")}와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,ans:K=>({fr:exact(PR[4],PR[4].P(K)).tot}),sol:K=>solGen(PR[4],PR[4].P(K),"tot"),num:K=>numArea(PR[4],PR[4].P(K))},
  {n:"넓이 36 → a",d:"다른 넓이 값으로 a 를 구해요.",K:{a:6},hl:["S"],text:K=>`곡선 ${hk("f","y = −x² + ax")}와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}가 ${kk(fr(K.a**3,6).str())}일 때, 양수 a의 값은?`,ans:K=>({fr:fr(K.a)}),sol:K=>[`S = a³/6 (이차함수와 x축 사이의 넓이)`,`a³/6 = ${fr(K.a**3,6).str()} → a³ = ${K.a**3}`,`a = <b>${K.a}</b>`],numRev:K=>bisect(a=>numArea(PR[4],{a}),0.1,20,K.a**3/6)},
  {n:"꼭짓점의 y좌표",d:"넓이로 a 를 구한 뒤 꼭짓점의 높이를 구해요.",K:{a:6},hl:["f"],text:K=>`곡선 ${hk("f","y = −x² + ax")}와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}가 ${kk(fr(K.a**3,6).str())}일 때, 이 곡선의 꼭짓점의 y좌표는? (a > 0)`,ans:K=>({fr:fr(K.a*K.a,4)}),sol:K=>[`S = a³/6 = ${fr(K.a**3,6).str()} → a = ${K.a}`,`y = −(x − a/2)² + a²/4 → 꼭짓점의 y좌표 = a²/4`,`= ${K.a}²/4 = <b>${fr(K.a*K.a,4).str()}</b>`],numRev:K=>{const a=bisect(a=>numArea(PR[4],{a}),0.1,20,K.a**3/6);return a*a/4}}]});
/* 0820 */
PR.push({id:"0820",tag:"",K0:{k:4,p:1,q:2},L:{k:"k",p:"왼쪽 경계 −p",q:"오른쪽 경계 q"},
 P:K=>({k:K.k,p:K.p,q:K.q}),f:(x,P)=>P.k*x*x*x,F:(x,P)=>P.k*x*x*x*x/4,FrA:(x,P)=>fr(P.k).mul(pw(x,4)).div(fr(4)),
 roots:P=>[0],rootsFr:P=>[Z],bounds:P=>[-P.p,P.q],boundsFr:P=>[fr(-P.p),fr(P.q)],xr:P=>[-P.p-1,P.q+1],fx:P=>"y = "+(P.k===1?"":P.k)+"x³",
 handles:P=>[{n:"k",x:P.q,y:P.k*P.q**3,set:(P,x,y)=>{P.k=clamp(Math.round(y/Math.pow(P.q,3)),1,8)}}],ok:K=>Number.isInteger(K.k)&&Number.isInteger(K.p)&&Number.isInteger(K.q)&&K.k>=1&&K.k<=8&&K.p>=1&&K.p<=4&&K.q>=1&&K.q<=4,
 area:K=>fr(K.k*(K.p**4+K.q**4),4),
 modes:[
  {n:"원래 문제",K:{k:4,p:1,q:2},hl:["S"],text:K=>`곡선 ${hk("f","y = kx³")}과 ${hk("axis","x축")} 및 두 직선 ${hk("lo","x = −"+K.p)}, ${hk("hi","x = "+K.q)}로 둘러싸인 도형의 ${hk("S","넓이","g")}가 ${kk(PR[5].area(K).str())}일 때, 양수 k의 값을 구하시오.`,ans:K=>({fr:fr(K.k)}),
   sol:K=>[`x < 0 에서 y = kx³ < 0 (x축 아래), x > 0 에서 y > 0 (x축 위) → 구간을 x = 0 에서 나눠요`,`S = −∫_{−${K.p}}^0 kx³ dx + ∫₀^${K.q} kx³ dx = k·${K.p}⁴/4 + k·${K.q}⁴/4 = ${fr(K.p**4+K.q**4,4).str()}·k`,`${fr(K.p**4+K.q**4,4).str()}·k = ${PR[5].area(K).str()} → k = <b>${K.k}</b>`],numRev:K=>bisect(k=>numArea(PR[5],{k,p:K.p,q:K.q}),0.01,50,PR[5].area(K).val())},
  {n:"k가 주어질 때 넓이",d:"조건을 뒤집어요: k 를 주고 넓이를 구해요.",K:{k:3,p:1,q:2},hl:["S"],text:K=>`곡선 ${hk("f","y = "+K.k+"x³")}과 ${hk("axis","x축")} 및 두 직선 ${hk("lo","x = −"+K.p)}, ${hk("hi","x = "+K.q)}로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,ans:K=>({fr:exact(PR[5],PR[5].P(K)).tot}),sol:K=>solGen(PR[5],PR[5].P(K),"tot"),num:K=>numArea(PR[5],PR[5].P(K))},
  {n:"구간 바꾸기",d:"구간을 바꿔서 넓이를 구해요.",K:{k:2,p:2,q:3},hl:["S"],text:K=>`곡선 ${hk("f","y = "+K.k+"x³")}과 ${hk("axis","x축")} 및 두 직선 ${hk("lo","x = −"+K.p)}, ${hk("hi","x = "+K.q)}로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,ans:K=>({fr:exact(PR[5],PR[5].P(K)).tot}),sol:K=>solGen(PR[5],PR[5].P(K),"tot"),num:K=>numArea(PR[5],PR[5].P(K))},
  {n:"x축 아래쪽 넓이",d:"x축 아래쪽 부분만 구해요.",K:{k:4,p:1,q:2},hl:["neg"],text:K=>`곡선 ${hk("f","y = "+K.k+"x³")}과 ${hk("axis","x축")} 및 두 직선 ${hk("lo","x = −"+K.p)}, ${hk("hi","x = "+K.q)}로 둘러싸인 도형 중 ${hk("neg","x축 아래쪽 부분","g")}의 넓이를 구하시오.`,ans:K=>({fr:exact(PR[5],PR[5].P(K)).neg}),sol:K=>solGen(PR[5],PR[5].P(K),"neg"),num:K=>numNeg(PR[5],PR[5].P(K))}]});
/* 0821 */
PR.push({id:"0821",tag:"",K0:{p:2,q:1},L:{p:"p (f=px²−qx)",q:"q"},
 P:K=>({p:K.p,q:K.q,t:1}),f:(x,P)=>P.p*x*x-P.q*x,F:(x,P)=>P.p*x*x*x/3-P.q*x*x/2,FrA:(x,P)=>fr(P.p).mul(pw(x,3)).div(fr(3)).sub(fr(P.q).mul(pw(x,2)).div(fr(2))),
 roots:P=>[0,P.q/P.p],rootsFr:P=>[Z,fr(P.q,P.p)],bounds:P=>[0,P.q/P.p],boundsFr:P=>[Z,fr(P.q,P.p)],xr:P=>[-1.2,Math.max(2.6,P.q/P.p+1.2)],fx:P=>"y = "+polyStr([[P.p,2],[-P.q,1]]),
 handles:P=>[{n:"t",x:P.t,y:0,set:(P,x)=>{P.t=clamp(Math.round(x*2)/2,-1,2.5)}}],ok:K=>Number.isInteger(K.p)&&Number.isInteger(K.q)&&K.p>=1&&K.p<=4&&K.q>=1&&K.q<=4,
 G:K=>{const a3=fr(K.p,3),a2=fr(K.q,2);return polyStr([[a3,3],[a2.neg(),2],[a3.sub(a2).neg(),0]])},
 modes:[
  {n:"원래 문제",K:{p:2,q:1},hl:["S"],text:K=>`함수 ${hk("f","f(x)")}가 모든 실수 x에 대하여 ${kk("∫₁ˣ f(t)dt = "+PR[6].G(K))}을 만족시킬 때, 곡선 y = f(x)와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,ans:K=>({fr:exact(PR[6],PR[6].P(K)).tot}),
   sol:K=>[`양변을 x 에 대해 미분: f(x) = ${polyStr([[K.p,2],[-K.q,1]])}  (f(x)=0 → x = 0, ${fr(K.q,K.p).str()})`,`[0, ${fr(K.q,K.p).str()}] 에서 f(x) ≤ 0 (x축 아래)`,`S = −∫₀^${fr(K.q,K.p).str()} f dx = <b>${exact(PR[6],PR[6].P(K)).tot.str()}</b>`],num:K=>numArea(PR[6],PR[6].P(K))},
  {n:"다른 적분 식",d:"적분 식을 바꿔서 같은 방식으로 넓이를 구해요.",K:{p:3,q:2},hl:["S"],text:K=>`함수 ${hk("f","f(x)")}가 모든 실수 x에 대하여 ${kk("∫₁ˣ f(t)dt = "+PR[6].G(K))}을 만족시킬 때, 곡선 y = f(x)와 ${hk("axis","x축")}으로 둘러싸인 도형의 ${hk("S","넓이","g")}를 구하시오.`,ans:K=>({fr:exact(PR[6],PR[6].P(K)).tot}),sol:K=>[`양변을 x 에 대해 미분: f(x) = ${polyStr([[K.p,2],[-K.q,1]])}`,`f(x)=0 → x = 0, ${fr(K.q,K.p).str()} ; 그 사이에서 x축 아래`,`S = −∫₀^${fr(K.q,K.p).str()} f dx = <b>${exact(PR[6],PR[6].P(K)).tot.str()}</b>`],num:K=>numArea(PR[6],PR[6].P(K))},
  {n:"f(2) 의 값",d:"넓이가 아니라 도함수로 f(2) 를 구해요.",K:{p:2,q:1},hl:["f"],text:K=>`함수 ${hk("f","f(x)")}가 모든 실수 x에 대하여 ${kk("∫₁ˣ f(t)dt = "+PR[6].G(K))}을 만족시킬 때, ${hk("f","f(2)")}의 값을 구하시오.`,ans:K=>({fr:fr(4*K.p-2*K.q)}),sol:K=>[`양변을 x 에 대해 미분 (미적분의 기본정리): f(x) = d/dx [${PR[6].G(K)}]`,`f(x) = ${polyStr([[K.p,2],[-K.q,1]])}`,`f(2) = ${4*K.p} − ${2*K.q} = <b>${4*K.p-2*K.q}</b>`],numRev:K=>{const P={p:K.p,q:K.q};const G=x=>PR[6].F(x,P)-PR[6].F(1,P);const h=1e-5;return (G(2+h)-G(2-h))/(2*h)}},
  {n:"x축과 만나는 점",d:"f(x)가 x축과 만나는 0이 아닌 점의 x좌표를 구해요.",K:{p:2,q:1},hl:["axis"],text:K=>`함수 ${hk("f","f(x)")}가 모든 실수 x에 대하여 ${kk("∫₁ˣ f(t)dt = "+PR[6].G(K))}을 만족시킬 때, 곡선 y = f(x)가 ${hk("axis","x축")}과 만나는 점 중 x좌표가 0이 아닌 점의 x좌표를 구하시오.`,ans:K=>({fr:fr(K.q,K.p)}),sol:K=>[`양변을 x 에 대해 미분: f(x) = ${polyStr([[K.p,2],[-K.q,1]])} = x(${polyStr([[K.p,1],[-K.q,0]])})`,`f(x) = 0 → x = 0 또는 x = ${fr(K.q,K.p).str()}`,`0이 아닌 교점의 x좌표 = <b>${fr(K.q,K.p).str()}</b>`],numRev:K=>K.q/K.p}]});
